#!/usr/bin/env python3

import re
from functools import cached_property
from itertools import chain, groupby
from operator import itemgetter
from statistics import mean
from typing import Any, Generator, Iterator

from ingredient_parser._constants import (
    APPROXIMATE_TOKENS,
    SINGULAR_TOKENS,
    STOP_WORDS,
)
from ingredient_parser._utils import consume, convert_to_pint_unit

from .dataclasses import (
    CompositeIngredientAmount,
    IngredientAmount,
    IngredientText,
    ParsedIngredient,
    _PartialIngredientAmount,
)

WORD_CHAR = re.compile(r"\w")


class PostProcessor:
    """Recipe ingredient sentence PostProcessor class.

    Performs the necessary postprocessing on the sentence tokens and labels and scores
    for the tokens after tagging with the CRF model in order to return a coherent
    structure of parsed information.

    Attributes
    ----------
    labels : list[str]
        List of labels for tokens.
    scores : list[float]
        Confidence associated with the label for each token.
    sentence : str
        Original ingredient sentence.
    tokens : list[str]
        List of tokens for original ingredient sentence.
    discard_isolated_stop_words : bool
        If True, isolated stop words are discarded from the name, preparation or
        comment fields. Default value is True.
    string_units : bool
        If True, return all IngredientAmount units as strings.
        If False, convert IngredientAmount units to pint.Unit objects where possible.
        Dfault is False.
    imperial_units : bool
        If True, use imperial units instead of US customary units for pint.Unit objects
        for the the following units: fluid ounce, cup, pint, quart, gallon.
        Default is False, which results in US customary units being used.
        This has no effect if string_units=True.
    consumed : list[int]
        List of indices of tokens consumed as part of setting the APPROXIMATE and
        SINGULAR flags. These tokens should not end up in the parsed output.
    """

    def __init__(
        self,
        sentence: str,
        tokens: list[str],
        labels: list[str],
        scores: list[float],
        discard_isolated_stop_words: bool = True,
        string_units: bool = False,
        imperial_units: bool = False,
    ):
        self.sentence = sentence
        self.tokens = tokens
        self.labels = labels
        self.scores = scores
        self.discard_isolated_stop_words = discard_isolated_stop_words
        self.string_units = string_units
        self.imperial_units = imperial_units
        self.consumed = []

    def __repr__(self) -> str:
        """__repr__ method

        Returns
        -------
        str
            String representation of initialised object
        """
        return f'PostProcessor("{self.sentence}")'

    def __str__(self) -> str:
        """__str__ method

        Returns
        -------
        str
            Human readable string representation of object
        """
        _str = [
            "Post-processed recipe ingredient sentence",
            f"\t{list(zip(self.tokens, self.labels))}",
        ]
        return "\n".join(_str)

    @cached_property
    def parsed(self) -> ParsedIngredient:
        """Return parsed ingredient data

        Returns
        -------
        ParsedIngredient
            Object containing structured data from sentence.
        """
        amounts = self._postprocess_amounts()
        size = self._postprocess("SIZE")
        name = self._postprocess("NAME")
        preparation = self._postprocess("PREP")
        comment = self._postprocess("COMMENT")

        return ParsedIngredient(
            name=name,
            size=size,
            amount=amounts,
            preparation=preparation,
            comment=comment,
            sentence=self.sentence,
        )

    def _postprocess(self, selected: str) -> IngredientText | None:
        """Process tokens, labels and scores with selected label into an
        IngredientText object.

        Parameters
        ----------
        selected : str
            Label of tokens to postprocess

        Returns
        -------
        IngredientText
            Object containing ingredient comment text and confidence
        """
        # Select indices of tokens, labels and scores for selected label
        # Do not include tokens, labels and scores in self.consumed
        idx = [
            i
            for i, label in enumerate(self.labels)
            if label in [selected, "PUNC"] and i not in self.consumed
        ]

        # Join consecutive tokens together and average their score
        parts = []
        confidence_parts = []
        for group in self._group_consecutive_idx(idx):
            idx = list(group)
            joined = " ".join([self.tokens[i] for i in idx])
            confidence = mean([self.scores[i] for i in idx])

            if self.discard_isolated_stop_words and joined in STOP_WORDS:
                # Discard part if it's a stop word
                continue

            parts.append(joined)
            confidence_parts.append(confidence)

        # Find the indices of the joined tokens list where the element
        # if a single punctuation mark or is the same as the previous element
        # in the list
        keep_idx = self._remove_isolated_punctuation_and_duplicate_indices(parts)
        parts = [parts[i] for i in keep_idx]
        confidence_parts = [confidence_parts[i] for i in keep_idx]

        # Join all the parts together into a single string and fix any
        # punctuation weirdness as a result.
        text = ", ".join(parts)
        text = self._fix_punctuation(text)

        if len(parts) == 0:
            return None

        return IngredientText(
            text=text,
            confidence=round(mean(confidence_parts), 6),
        )

    def _postprocess_amounts(self) -> list[IngredientAmount]:
        """Process tokens, labels and scores into IngredientAmount objects, by combining
        QTY labels with any following UNIT labels, up to the next QTY label.

        The confidence is the average confidence of all labels in the IngredientGroup.

        A number of special cases are considered before the default processing:
        1. "sizable unit" pattern
        2. "composite amounts" pattern

        Returns
        -------
        list[IngredientAmount]
            List of IngredientAmount objects
        """

        funcs = [
            self._sizable_unit_pattern,
            self._composite_amounts_pattern,
            self._fallback_pattern,
        ]

        amounts = []
        for func in funcs:
            idx = self._unconsumed(list(range(len(self.tokens))))
            tokens = self._unconsumed(self.tokens)
            labels = self._unconsumed(self.labels)
            scores = self._unconsumed(self.scores)

            parsed_amounts = func(idx, tokens, labels, scores)
            amounts.extend(parsed_amounts)

        return sorted(amounts, key=lambda x: x._starting_index)

    def _unconsumed(self, list_: list[Any]) -> list[Any]:
        """Return elements from list whose index is not in the list of consumed
        indices

        Parameters
        ----------
        list_ : list[Any]
            List of items to remove consumed elements from

        Returns
        -------
        list[Any]
            List of items without consumed elements
        """
        return [el for i, el in enumerate(list_) if i not in self.consumed]

    def _fix_punctuation(self, text: str) -> str:
        """Fix some common punctuation errors that result from combining tokens of the
        same label together.

        Parameters
        ----------
        text : str
            Text resulting from combining tokens with same label

        Returns
        -------
        str
            Text, with punctuation errors fixed

        Examples
        --------
        >>> p = PostProcessor("", [], [], [])
        >>> p._fix_punctuation(", some words ( inside ),")
        "some words (inside)"

        >>> p = PostProcessor("", [], [], [])
        >>> p._fix_punctuation("(unmatched parenthesis (inside)(")
        "unmatched parenthesis (inside)"
        """
        if text == "":
            return text

        # Correct space following open parens or before close parens
        text = text.replace("( ", "(").replace(" )", ")")

        # Correct space preceeding various punctuation
        for punc in [",", ":", ";"]:
            text = text.replace(f" {punc}", punc)

        # Remove parentheses that aren't part of a matching pair
        idx_to_remove = []
        stack = []
        for i, char in enumerate(text):
            if char in ["(", "["]:
                # Add index to stack when we find an opening parens
                stack.append(i)
            elif char in [")", "]"]:
                if len(stack) == 0:
                    # If the stack is empty, we've found a dangling closing parens
                    idx_to_remove.append(i)
                else:
                    # Remove last added index from stack when we find a closing parens
                    stack.pop()

        # Insert anything left in stack into idx_to_remove
        idx_to_remove.extend(stack)
        text = "".join(char for i, char in enumerate(text) if i not in idx_to_remove)

        # Remove leading comma, colon, semi-colon, hyphen
        while text[0] in [",", ";", ":", "-"]:
            text = text[1:].strip()

        # Remove trailing comma, colon, semi-colon, hypehn
        while text[-1] in [",", ";", ":", "-"]:
            text = text[:-1].strip()

        return text.strip()

    def _remove_isolated_punctuation_and_duplicate_indices(
        self, parts: list[str]
    ) -> list[int]:
        """Find elements in list that comprise a single punctuation character or are a
        duplicate of the previous element and discard their indices.

        Parameters
        ----------
        parts : list[str]
            List of tokens with single label, grouped if consecutive

        Returns
        -------
        list[int]
            Indices of elements in parts to keep

        Examples
        --------
        >>> p = PostProcessor("", [], [], [])
        >>> p._remove_isolated_punctuation_and_duplicate_indices(
            ["word", ",", "with, comma"],
        )
        [0, 2]

        >>> p = PostProcessor("", [], [], [])
        >>> p._remove_isolated_punctuation_and_duplicate_indices(
            ["word", "word", "another"],
        )
        [0, 2]
        """
        # Only keep a part if contains a word character
        idx_to_keep = []
        for i, part in enumerate(parts):
            if i == 0 and WORD_CHAR.search(part):
                idx_to_keep.append(i)
            elif WORD_CHAR.search(part) and part != parts[i - 1]:
                idx_to_keep.append(i)

        return idx_to_keep

    def _group_consecutive_idx(
        self, idx: list[int]
    ) -> Generator[Iterator[int], None, None]:
        """Yield groups of consecutive indices

        Given a list of integers, yield groups of integers where the value of each in a
        group is adjacent to the previous element's value.

        Parameters
        ----------
        idx : list[int]
            List of indices

        Yields
        ------
        list[list[int]]
            List of lists, where each sub-list contains consecutive indices

        Examples
        --------
        >>> groups = group_consecutive_idx([0, 1, 2, 4, 5, 6, 8, 9])
        >>> [list(g) for g in groups]
        [[0, 1, 2], [4, 5, 6], [8, 9]]
        """
        for _, g in groupby(enumerate(idx), key=lambda x: x[0] - x[1]):
            yield map(itemgetter(1), g)

    def _sizable_unit_pattern(
        self, idx: list[int], tokens: list[str], labels: list[str], scores: list[float]
    ) -> list[IngredientAmount]:
        """Identify sentences which match the pattern where there is a
        quantity-unit pair split by one or more quantity-unit pairs e.g.

        * 1 28 ounce can
        * 2 17.3 oz (484g) package

        Return the correct sets of quantities and units, or an empty list.

        For example, for the sentence: 1 28 ounce can; the correct amounts are:
        [
            IngredientAmount(quantity="1", unit="can", score=0.x...),
            IngredientAmount(quantity="28", unit="ounce", score=0.x...),
        ]

        Parameters
        ----------
        idx : list[int]
            List of indices of the tokens/labels/scores in the full tokenizsed sentence
        tokens : list[str]
            Tokens for input sentence
        labels : list[str]
            Labels for input sentence tokens
        scores : list[float]
            Scores for each label

        Returns
        -------
        list[IngredientAmount]
            List of IngredientAmount objects
        """
        # We assume that the pattern will not be longer than the longest list
        # defined here.
        patterns = [
            ["QTY", "QTY", "UNIT", "QTY", "UNIT", "QTY", "UNIT", "UNIT"],
            ["QTY", "QTY", "UNIT", "QTY", "UNIT", "UNIT"],
            ["QTY", "QTY", "UNIT", "UNIT"],
        ]

        # List of possible units at end of pattern that constitute a match
        end_units = [
            "bag",
            "block",
            "box",
            "can",
            "envelope",
            "jar",
            "package",
            "packet",
            "piece",
            "sachet",
            "slice",
            "tin",
        ]

        amounts = []
        for pattern in patterns:
            for match in self._match_pattern(labels, pattern, ignore_other_labels=True):
                # If the pattern ends with one of end_units, we have found a match for
                # this pattern!
                if tokens[match[-1]] in end_units:
                    # Get tokens and scores that are part of match
                    matching_tokens = [tokens[i] for i in match]
                    matching_scores = [scores[i] for i in match]

                    # Keep track of indices of matching elements so we don't use them
                    # again elsewhere
                    self.consumed.extend([idx[i] for i in match])

                    # The first amount is made up of the first and last items
                    # Note that this cannot be singular, but may be approximate
                    quantity = matching_tokens.pop(0)
                    unit = matching_tokens.pop(-1)
                    text = " ".join((quantity, unit)).strip()

                    if not self.string_units:
                        # If the unit is recognised in the pint unit registry, use
                        # a pint.Unit object instead of a string. This has the benefit
                        # of simplifying alternative unit representations into a single
                        # common representation
                        unit = convert_to_pint_unit(unit, self.imperial_units)

                    first = IngredientAmount(
                        quantity=quantity,
                        unit=unit,
                        text=text,
                        confidence=round(
                            mean([matching_scores.pop(0), matching_scores.pop(-1)]), 6
                        ),
                        starting_index=idx[match[0]],
                        APPROXIMATE=self._is_approximate(match[0], tokens, labels, idx),
                    )
                    amounts.append(first)
                    # Pop the first and last items from the list of matching indices
                    _ = match.pop(0)
                    _ = match.pop(-1)

                    # Now create the IngredientAmount objects for the pairs in between
                    # the first and last items
                    for i in range(0, len(matching_tokens), 2):
                        quantity = matching_tokens[i]
                        unit = matching_tokens[i + 1]
                        text = " ".join((quantity, unit)).strip()
                        confidence = mean(matching_scores[i : i + 1])

                        if not self.string_units:
                            # Conver to pint.Unit if appropriate
                            unit = convert_to_pint_unit(unit, self.imperial_units)

                        # If the first amount (e.g. 1 can) is approximate, so are all
                        # the pairs in between
                        amount = IngredientAmount(
                            quantity=quantity,
                            unit=unit,
                            text=text,
                            confidence=round(confidence, 6),
                            starting_index=idx[match[i]],
                            SINGULAR=True,
                            APPROXIMATE=first.APPROXIMATE,
                        )
                        amounts.append(amount)

        return amounts

    def _composite_amounts_pattern(
        self, idx: list[int], tokens: list[str], labels: list[str], scores: list[float]
    ) -> list[CompositeIngredientAmount]:
        """Identify sentences which match the pattern where there are composite amounts,
        i.e. adjacent amounts that need to be considered together:

        * 1 lb 2 oz
        * 1 pint 2 fl oz

        Return a compositive amount object made from the adjacent amounts.

        For example, for the sentence: 1 lb 2 oz ...; the composite amount is:
        CompositeAmount(
            amounts=[
                IngredientAmount(quantity="1", unit="lb", score=0.x...),
                IngredientAmount(quantity="2", unit="oz", score=0.x...),
            ],
            join=""
        )

        Parameters
        ----------
        idx : list[int]
            List of indices of the tokens/labels/scores in the full tokenizsed sentence
        tokens : list[str]
            Tokens for input sentence
        labels : list[str]
            Labels for input sentence tokens
        scores : list[float]
            Scores for each label

        Returns
        -------
        list[CompositeIngredientAmount]
            List of IngredientAmount objects
        """
        # Define patterns based on labels.
        # Assumes that only "x lb y oz" and "x pint y fl oz" patterns
        patterns = [
            ["QTY", "UNIT", "QTY", "UNIT", "UNIT"],
            ["QTY", "UNIT", "QTY", "UNIT"],
        ]

        # List of possible units for first and second amount matched
        first_unit = {"lb", "pound", "pt", "pint"}
        last_unit = {"oz", "ounce"}

        composite_amounts = []
        for pattern in patterns:
            for match in self._match_pattern(
                labels, pattern, ignore_other_labels=False
            ):
                # Check units match known patterns
                first_unit_idx = match[1]
                last_unit_idx = match[-1]
                if (
                    tokens[first_unit_idx] in first_unit
                    and tokens[last_unit_idx] in last_unit
                ):
                    # First amount
                    quantity_1 = tokens[match[0]]
                    unit_1 = tokens[match[1]]
                    text_1 = " ".join((quantity_1, unit_1)).strip()
                    if not self.string_units:
                        # Convert to pint.Unit if appropriate
                        unit_1 = convert_to_pint_unit(unit_1, self.imperial_units)

                    first_amount = IngredientAmount(
                        quantity=quantity_1,
                        unit=unit_1,
                        text=text_1,
                        confidence=round(mean([scores[i] for i in match[0:2]]), 6),
                        starting_index=idx[first_unit_idx - 1],
                    )
                    # Second amount
                    quantity_2 = tokens[match[2]]
                    unit_2 = " ".join([tokens[i] for i in match[3:]])
                    text_2 = " ".join((quantity_2, unit_2)).strip()
                    if not self.string_units:
                        # Convert to pint.Unit if appropriate
                        unit_2 = convert_to_pint_unit(unit_2, self.imperial_units)

                    second_amount = IngredientAmount(
                        quantity=quantity_2,
                        unit=unit_2,
                        text=text_2,
                        confidence=round(mean([scores[i] for i in match[3:]]), 6),
                        starting_index=idx[last_unit_idx - 1],
                    )
                    composite_amounts.append(
                        CompositeIngredientAmount(
                            amounts=[first_amount, second_amount],
                            join="",
                        )
                    )

                    # Keep track of indices of matching elements so we don't use them
                    # again elsewhere
                    self.consumed.extend([idx[i] for i in match])

        return composite_amounts

    def _match_pattern(
        self, labels: list[str], pattern: list[str], ignore_other_labels: bool = True
    ) -> list[list[int]]:
        """Find a pattern of labels and return the indices of the labels that match the
        pattern. The pattern matching ignores labels that are not part of the pattern.

        For example, consider the sentence:
        One 15-ounce can diced tomatoes, with liquid

        It has the tokens and labels:
        ['1', '15', 'ounce', 'can', 'diced', 'tomatoes', ',', 'with', 'liquid']
        ['QTY', 'QTY', 'UNIT', 'UNIT', 'COMMENT', 'NAME', 'COMMA', 'COMMENT', 'COMMENT']

        If we search for the pattern:
        ["QTY", "QTY", "UNIT", "UNIT"]

        Then we get:
        [[0, 1, 2, 3]]

        Parameters
        ----------
        labels : list[str]
            List of labels of find pattern
        pattern : list[str]
            Pattern to match inside labels.
        ignore_other_labels : bool
            If True, the pattern matching will ignore any labels not found in pattern
            meaning the indices of the match may not be consecutive.
            If False, the pattern must be found without any interruptions in the
            labels list.

        Returns
        -------
        list[list[int]]
            List of label index lists that match the pattern.
        """
        plen = len(pattern)
        plabels = set(pattern)

        if ignore_other_labels:
            # Select just the labels and indices of labels that are in the pattern.
            lbls = [label for label in labels if label in plabels]
            idx = [i for i, label in enumerate(labels) if label in plabels]
        else:
            # Consider all labels
            lbls = labels
            idx = [i for i, _ in enumerate(labels)]

        if len(pattern) > len(lbls):
            # We can never find a match.
            return []

        matches = []
        indices = iter(range(len(lbls)))
        for i in indices:
            # Short circuit: If the lbls[i] is not equal to the first element
            # of pattern skip to next iteration
            if lbls[i] == pattern[0] and lbls[i : i + plen] == pattern:
                matches.append(idx[i : i + plen])
                # Advance iterator to prevent overlapping matches
                consume(indices, plen)

        return matches

    def _fallback_pattern(
        self,
        idx: list[int],
        tokens: list[str],
        labels: list[str],
        scores: list[float],
    ) -> list[IngredientAmount]:
        """Fallback pattern for grouping quantities and units into amounts.
        This is done simply by grouping a QTY with all following UNIT until
        the next QTY.

        A special case is the for when the token "dozen" is labelled as QTY and
        it follows a QTY. In this case, the quantity of previous amount is
        modified to include "dozen".

        Parameters
        ----------
        idx : list[int]
            List of indices of the tokens/labels/scores in the full tokenizsed sentence
        tokens : list[str]
            Tokens for input sentence
        labels : list[str]
            Labels for input sentence tokens
        scores : list[float]
            Scores for each label

        Returns
        -------
        list[IngredientAmount]
            List of IngredientAmount objects
        """
        amounts = []

        # If a new amount starts with the token after a (, / or [ then it we assume it
        # is related to the previous amount
        # We use idx+1 here so we can check the index in the iteration a new amount is
        # created and avoid needing to check things like i >= 0
        related_idx = [
            idx + 1 for idx, tok in enumerate(tokens) if tok in ["(", "/", "["]
        ]

        for i, (token, label, score) in enumerate(zip(tokens, labels, scores)):
            if label == "QTY":
                # Whenever we come across a new QTY, create new IngredientAmount,
                # unless the token is "dozen" and the previous label was QTY, in which
                # case we combine modify the quantity of the previous amount.
                if token == "dozen" and labels[i - 1] == "QTY":
                    amounts[-1].quantity = amounts[-1].quantity + " dozen"
                    amounts[-1].confidence.append(score)
                else:
                    amounts.append(
                        _PartialIngredientAmount(
                            quantity=token,
                            unit=[],
                            confidence=[score],
                            _starting_index=idx[i],
                            related_to_previous=i in related_idx,
                        )
                    )

            if label == "UNIT":
                if amounts == []:
                    # Not come across a QTY yet, so create IngredientAmount
                    # with no quantity
                    amounts.append(
                        _PartialIngredientAmount(
                            quantity="",
                            unit=[],
                            confidence=[score],
                            _starting_index=idx[i],
                        )
                    )

                if i > 0 and tokens[i - 1] == "," and amounts[-1].unit != []:
                    # If the previous token was a comma, and the last amount has a unit,
                    # append comma to unit of last IngredientAmount
                    amounts[-1].unit.append(",")

                # Append token and score for unit to last IngredientAmount
                amounts[-1].unit.append(token)
                amounts[-1].confidence.append(score)

            # Check if any flags should be set
            if self._is_approximate(i, tokens, labels, idx):
                amounts[-1].APPROXIMATE = True

            if self._is_singular(i, tokens, labels, idx):
                amounts[-1].SINGULAR = True

            if self._is_singular_and_approximate(i, tokens, labels, idx):
                amounts[-1].APPROXIMATE = True
                amounts[-1].SINGULAR = True

        # Set APPROXIMATE and SINGULAR flags to be the same for all related amounts
        amounts = self._distribute_related_flags(amounts)

        # Loop through amounts list to fix unit and confidence
        # Unit needs converting to a string
        # Confidence needs averaging
        # Then convert to IngredientAmount object
        processed_amounts = []
        for amount in amounts:
            unit = " ".join(amount.unit)
            text = " ".join((amount.quantity, unit)).strip()

            if not self.string_units:
                # If the unit is recognised in the pint unit registry, use
                # a pint.Unit object instead of a string. This has the benefit of
                # simplifying alternative unit representations into a single
                # common representation
                unit = convert_to_pint_unit(unit, self.imperial_units)

            # Convert to an IngredientAmount object for returning
            processed_amounts.append(
                IngredientAmount(
                    quantity=amount.quantity,
                    unit=unit,
                    text=text,
                    confidence=round(mean(amount.confidence), 6),
                    starting_index=amount._starting_index,
                    APPROXIMATE=amount.APPROXIMATE,
                    SINGULAR=amount.SINGULAR,
                )
            )

        return processed_amounts

    def _is_approximate(
        self, i: int, tokens: list[str], labels: list[str], idx: list[int]
    ) -> bool:
        """Return True is token at current index is approximate, determined
        by the token label being QTY and the previous token being in a list of
        approximate tokens.

        If returning True, also add index of i - 1 token to self.consumed list.

        Parameters
        ----------
        i : int
            Index of current token
        tokens : list[str]
            List of all tokens
        labels : list[str]
            List of all token labels
        idx : list[int]
            List of indices of the tokens/labels/scores in the full tokenizsed sentence

        Returns
        -------
        bool
            True if current token is approximate

        Examples
        --------
        >>> p = PostProcessor("", [], [], [])
        >>> p._is_approximate(
            1,
            ["about", "3", "cups"],
            ["COMMENT", "QTY", "UNIT"],
            [0, 1, 2]
        )
        True

        >>> p = PostProcessor("", [], [], [])
        >>> p._is_approximate(
            1,
            ["approx.", "250", "g"],
            ["COMMENT", "QTY", "UNIT"],
            [0, 1, 2]
        )
        True
        """
        if i == 0:
            return False

        if labels[i] == "QTY" and tokens[i - 1].lower() in APPROXIMATE_TOKENS:
            # Mark i - 1 element as consumed
            self.consumed.append(idx[i - 1])
            return True

        return False

    def _is_singular(
        self, i: int, tokens: list[str], labels: list[str], idx: list[int]
    ) -> bool:
        """Return True is token at current index is singular, determined
        by the token label being UNIT and the next token being in a list of
        singular tokens.

        If returning True, also add index of i + 1 token to self.consumed list.

        Parameters
        ----------
        i : int
            Index of current token
        tokens : list[str]
            List of all tokens
        labels : list[str]
            List of all token labels
        idx : list[int]
            List of indices of the tokens/labels/scores in the full tokenizsed sentence

        Returns
        -------
        bool
            True if current token is singular

        Examples
        --------
        >>> p = PostProcessor("", [], [], [])
        >>> p._is_singular(
            1,
            ["3", "oz", "each"],
            ["QTY", "UNIT", "COMMENT"],
            [0, 1, 2]
        )
        True
        """
        if i == len(tokens) - 1:
            return False

        if labels[i] == "UNIT" and tokens[i + 1].lower() in SINGULAR_TOKENS:
            # Mark i - 1 element as consumed
            self.consumed.append(idx[i + 1])
            return True

        if i == len(tokens) - 2:
            return False

        # Case where the amonut is in brackets
        if (
            labels[i] == "UNIT"
            and tokens[i + 1] in [")", "]"]
            and tokens[i + 2].lower() in SINGULAR_TOKENS
        ):
            # Mark i - 1 element as consumed
            self.consumed.append(idx[i + 2])
            return True

        return False

    def _is_singular_and_approximate(
        self, i: int, tokens: list[str], labels: list[str], idx: list[int]
    ) -> bool:
        """Return True if the current token is approximate and singular, determined
        by the token label being QTY and is preceded by a token in a list of singular
        tokens, then token in a list of approximate tokens.

        If returning True, also add index of i - 1 and i - 2 tokens to
        self.consumed list.

        e.g. each nearly 3 ...

        Parameters
        ----------
        i : int
            Index of current token
        tokens : list[str]
            List of all tokens
        labels : list[str]
            List of all token labels
        idx : list[int]
            List of indices of the tokens/labels/scores in the full tokenizsed sentence

        Returns
        -------
        bool
            True if current token is singular

        Examples
        --------
        >>> p = PostProcessor("", [], [], [])
        >>> p._is_approximate(
            1,
            ["nearly", "3", "oz", "each"],
            ["COMMENT", "QTY", "UNIT", "COMMENT"],
            [0, 1, 2, 3]
        )
        True
        """
        if i < 2:
            return False

        if (
            labels[i] == "QTY"
            and tokens[i - 1].lower() in APPROXIMATE_TOKENS
            and tokens[i - 2].lower() in SINGULAR_TOKENS
        ):
            # Mark i - 1 and i - 2 elements as consumed
            self.consumed.append(idx[i - 1])
            self.consumed.append(idx[i - 2])
            return True

        return False

    def _distribute_related_flags(
        self, amounts: list[_PartialIngredientAmount]
    ) -> list[_PartialIngredientAmount]:
        """Where amounts are related to the previous, ensure that all related amounts
        have the same flags set.

        Parameters
        ----------
        amounts : list[_PartialIngredientAmount]
            List of amounts

        Returns
        -------
        list[_PartialIngredientAmount]
            List of amount with all related amounts having the same flags
        """
        # Group amounts into related groups
        grouped = []
        for amount in amounts:
            if grouped and amount.related_to_previous:
                grouped[-1].append(amount)
            else:
                grouped.append([amount])

        # Set flags for all amounts in group if any amount has flag set
        for group in grouped:
            if any(am.APPROXIMATE for am in group):
                for am in group:
                    am.APPROXIMATE = True

            if any(am.SINGULAR for am in group):
                for am in group:
                    am.SINGULAR = True

        # Flatten list for return
        return list(chain.from_iterable(grouped))
