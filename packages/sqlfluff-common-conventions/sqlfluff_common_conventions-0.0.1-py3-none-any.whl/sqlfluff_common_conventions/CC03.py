"""Implementation of Rule CC03."""

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_CC03(BaseRule):
    """Do not have a date column that does not end with `_date`.

    **Anti-pattern**

    .. code-block:: sql

        create or replace table tbl (
            created date
        )

    **Best practice**

    End date columns with `_date`.

    .. code-block:: sql

        create or replace table tbl (
            created_date date
        )
    """

    groups = ("all",)

    crawl_behaviour = SegmentSeekerCrawler(
        {
            "column_definition",
            "select_clause_element",
        }
    )
    is_fix_compatible = False

    def _eval(self, context: RuleContext):
        """Find rule violations and provide fixes."""

        select_clause = (
            context.segment.is_type("select_clause_element")
            and context.segment.segments[0].is_type("function")
            and context.segment.segments[0].segments[0].raw.lower() == "cast"
            and context.segment.segments[-1].is_type("alias_expression")
        )

        column_definition = context.segment.is_type("column_definition")

        if not (select_clause or column_definition):
            return

        if select_clause:
            identifier = list(
                filter(
                    lambda x: x.is_type("identifier"),
                    context.segment.segments[-1].segments,
                )
            )
            datatype = list(
                filter(
                    lambda x: x.is_type("data_type"),
                    context.segment.segments[0].segments[-1].segments,
                )
            )

        else:
            identifier = list(
                filter(lambda x: x.is_type("identifier"), context.segment.segments)
            )
            datatype = list(
                filter(
                    lambda x: x.is_type("data_type"),
                    context.segment.segments,
                )
            )

        identifier = identifier[0].raw.lower()
        datatype = datatype[0].raw.lower()

        if datatype in ["date"] and not (identifier.endswith("_date")):
            return LintResult(
                anchor=context.segment,
                description="Date column does not end with `_date`.",
            )
