from django.test import TestCase
from django.urls import reverse


class PagesTests(TestCase):
    def test_home_page_has_links_to_other_pages(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")
        self.assertContains(response, "Contacts")
        self.assertContains(response, reverse("pages:about"))
        self.assertContains(response, reverse("pages:contacts"))

    def test_inner_pages_have_link_to_home(self):
        for page_name in ("pages:about", "pages:contacts"):
            response = self.client.get(reverse(page_name))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, reverse("pages:home"))
