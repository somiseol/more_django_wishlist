from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')  # request to make
        response = self.client.get(home_page_url)  # will run server in the background and make the request, then saves response

        # make assertions about the saved response
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'you have no places in your wishlist')


class TestWishList(TestCase):

    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, "Tokyo")
        self.assertContains(response, "New York")

        self.assertNotContains(response, "San Francisco")
        self.assertNotContains(response, "Moab")


# test for: 'visited' page has 'no places visited' message if db is empty
class TestVisitedPage(TestCase):
    page_url = reverse('places_visited')

    def test_visited_page_shows_empty_list_message_for_empy_database(self):
        response = self.client.get(self.page_url)

        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'no places visited yet')


class VisitedList(TestCase):
    page_url = reverse('places_visited')
    fixtures = ['test_places']

    def test_visited_places_not_contains_visited_places(self):
        response = self.client.get(self.page_url)

        self.assertContains(response, "San Francisco")
        self.assertContains(response, "Moab")
        
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')


class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)  # follow is let redirect after POST

        self.assertTemplateUsed('travel_wishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places))  # check only 1 place was added

        tokyo_from_response = response_places[0]
        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_database, tokyo_from_response)

class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed('travel_wishlist/wishlist')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    
    def test_visit_nonexisten_place(self):
        url = reverse('place_was_visited', args=(12345, ))
        response = self.client.post(url, follow=True)

        self.assertEqual(404, response.status_code)
