"""Common helper code for tests"""

import aldjemy.core
from django.test import RequestFactory
from test_plus.test import TestCase, APITestCase

from .factories import ProcessedFormDataFactory
from ..models import Case, CaseAwareProject
from variants.helpers import SQLALCHEMY_ENGINE


class TestBase(TestCase):
    """Base class for all tests."""


class ViewTestBaseMixin:
    def setUp(self):
        super().setUp()
        self.maxDiff = None  # show full diff

        self.request_factory = RequestFactory()

        # setup super user
        self.user = self.make_user("superuser")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()


class ApiViewTestBase(ViewTestBaseMixin, APITestCase):
    """Base class for API view testing (and file export)"""


class ViewTestBase(ViewTestBaseMixin, TestCase):
    """Base class for UI view testing (and file export)"""


class QueryTestBase(TestBase):
    """Base class with helper code for model queries."""

    def run_get_query(self, model, query_data, assert_raises=None):
        """Run query using ``get()``."""
        if assert_raises:
            with self.assertRaises(assert_raises):
                model.objects.get(**query_data)
        else:
            return model.objects.get(**query_data)

    def run_filter_query(self, model, query_data, length):
        """Run query using ``filter()``."""
        results = model.objects.filter(**query_data)
        self.assertEquals(length, len(results))
        return results


class SupportQueryTestBase(TestBase):
    """Base class for model support queries."""

    def _get_fetch_and_query(self, query_class, cleaned_data_patch, query_type="case"):
        engine = SQLALCHEMY_ENGINE

        def fetch_case_and_query():
            """Helper function that fetches the ``case`` by UUID and then generates the
            appropriate query.
            """
            if query_type == "case":
                if not "case_uuid" in cleaned_data_patch:
                    obj = Case.objects.first()
                else:
                    obj = Case.objects.get(sodar_uuid=cleaned_data_patch["case_uuid"])
            else:  # query_type == "project"
                obj = CaseAwareProject.objects.first()
            patched_cleaned_data = {
                **vars(ProcessedFormDataFactory(names=obj.get_members())),
                **cleaned_data_patch,
            }
            previous_query = patched_cleaned_data.get("filter_job_id", None)
            patched_cleaned_data["sodar_uuid"] = obj.sodar_uuid
            if previous_query:
                query = query_class(obj, engine, previous_query)
            else:
                query = query_class(obj, engine)
            return query.run(patched_cleaned_data)

        return fetch_case_and_query

    def run_query(
        self, query_class, cleaned_data_patch, length, assert_raises=None, query_type="case"
    ):
        """Run query returning a collection of filtration results with ``query_class``.

        This is a helper to be called in all ``test_*()`` functions.  It is a shortcut
        to the following:

        - Create a query kwargs ``dict`` by patching ``self.__class__.base_cleaned_data``
          with ``patch_cleaned_data``.
        - Perform the query.
        - Assert that exactly ``length`` elements are returned (and return list of these
          elements for further testing).
        - If ``assert_raises`` evaluates as ``True`` then instead of checking the result
          length and returning a list of elements, assert that an exception of type
          ``assert_raises`` is raised.
        """
        fetch_case_and_query = self._get_fetch_and_query(
            query_class, cleaned_data_patch, query_type
        )
        if assert_raises:
            with self.assertRaises(assert_raises):
                fetch_case_and_query()
        else:
            results = list(fetch_case_and_query())
            self.assertEquals(length, len(results))
            return results

    def run_count_query(
        self, query_class, kwargs_patch, length, assert_raises=None, query_type="case"
    ):
        """Run query returning a result record count instead of result records."""
        fetch_case_and_query = self._get_fetch_and_query(query_class, kwargs_patch, query_type)
        if assert_raises:
            with self.assertRaises(assert_raises):
                fetch_case_and_query()
        else:
            result = fetch_case_and_query()
            self.assertEquals(length, result)
            return result
