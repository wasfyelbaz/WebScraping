from bs4 import BeautifulSoup


class ExtractCars:

    source_code = None
    base_url = None
    cars_list = []

    def __int__(self):

        pass

    def run(self):

        self.cars_list = []

        cars_names = self.extract_cars_names(self.source_code)
        #print(len(cars_names))

        cars_prices = self.extract_cars_prices(self.source_code)
        #print(len(cars_prices))

        cars_mileage = self.extract_cars_mileage(self.source_code)
        #print(len(cars_mileage))

        cars_transmission = self.extract_cars_transmission(self.source_code)
        #print(len(cars_transmission))

        cars_offer_type = self.extract_cars_offer_type(self.source_code)
        #print(len(cars_offer_type))

        cars_previous_owners = self.extract_cars_previous_owners(self.source_code)
        #print(len(cars_previous_owners))

        cars_first_registration = self.extract_cars_first_registration(self.source_code)
        #print(len(cars_first_registration))

        cars_links = self.extract_cars_links(self.source_code)
        #print(len(cars_links))

        for car_name, \
            car_price, \
            car_mileage, \
            car_transmission, \
            car_offer_type, \
            car_previous_owners, \
            car_first_registration,\
            car_link in zip(cars_names,
                                          cars_prices,
                                          cars_mileage,
                                          cars_transmission,
                                          cars_offer_type,
                                          cars_previous_owners,
                                          cars_first_registration,
                                          cars_links):

            car = {
                "name": car_name,
                "price": car_price,
                "mileage": car_mileage,
                "transmission": car_transmission,
                "offer_type": car_offer_type,
                "previous_owners": car_previous_owners,
                "first_registration": car_first_registration,
                "link": self.base_url + car_link
            }

            self.cars_list.append(car)

    def get_int_number(self, string):
        # Get integer from string.
        number = list(string.strip())

        int_number = ''
        for char in number:

            try:
                int(char)
                int_number += char

            except ValueError:
                pass

        if int_number == "":
            return None

        return int(int_number)

    def is_date(self, string):

        allowed_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"]
        test_string = list(string)

        for char in test_string:
            if char in allowed_char:
                pass
            else:
                return False

        return True

    def extract_cars_names(self, src_code):
        # Extract cars names.
        cars_names = []

        h2_tags = src_code.find_all("h2")
        del h2_tags[0]
        del h2_tags[-1]

        for index, h2_tag in enumerate(h2_tags):

            try:
                if index % 2 == 0:
                    car_name = h2_tag.text + ' / ' + h2_tags[index + 1].text
                    cars_names.append(car_name)
            except IndexError:
                pass

        return cars_names

    def extract_cars_prices(self, src_code):
        # Extract cars prices.
        cars_prices = []

        price_span_tags = src_code.find_all("span", {"data-item-name": "price"})

        for index, span_tag in enumerate(price_span_tags):
            car_price = self.get_int_number(span_tag.text)
            cars_prices.append(car_price)
            # print(f"{price:,}")

        return cars_prices

    def extract_cars_mileage(self, src_code):
        # Extract cars mileage.
        cars_mileage = []

        mileage_li_tags = src_code.find_all("li", {"data-type": "mileage"})

        for li_tag in mileage_li_tags:

            car_mileage = self.get_int_number(li_tag.text)

            if car_mileage is None:
                car_mileage = "Unknown"

            cars_mileage.append(car_mileage)

        return cars_mileage

    def extract_cars_transmission(self, src_code):
        # Extract cars transmission.
        cars_transmission = []

        transmission_li_tags = src_code.find_all("li", {"data-type": "transmission-type"})

        for li_tag in transmission_li_tags:

            car_transmission = li_tag.text.strip()

            if car_transmission == "":
                car_transmission = "Unknown"

            cars_transmission.append(car_transmission)

        return cars_transmission

    def extract_cars_offer_type(self, src_code):
        # Extract cars offer type.
        cars_offer_type = []

        offer_type_li_tags = src_code.find_all("li", {"data-type": "offer-type"})

        for li_tag in offer_type_li_tags:

            car_offer_type = li_tag.text.strip()

            if car_offer_type == "":
                car_offer_type = "Unknown"

            cars_offer_type.append(car_offer_type)

        return cars_offer_type

    def extract_cars_previous_owners(self, src_code):
        # Extract cars previous owners.
        cars_previous_owners = []

        previous_owners_li_tags = src_code.find_all("li", {"data-type": "previous-owners"})

        for li_tag in previous_owners_li_tags:

            car_previous_owners = self.get_int_number(li_tag.text)

            if car_previous_owners == "" or car_previous_owners is None:
                car_previous_owners = "Unknown"

            cars_previous_owners.append(car_previous_owners)

        return cars_previous_owners

    def extract_cars_first_registration(self, src_code):
        # Extract cars first registration.
        cars_first_registration = []

        first_registration_li_tags = src_code.find_all("li", {"data-type": "first-registration"})

        for li_tag in first_registration_li_tags:

            car_first_registration = li_tag.text.strip()

            if self.is_date(car_first_registration):
                pass

            else:
                car_first_registration = "Unknown"

            cars_first_registration.append(car_first_registration)

        return cars_first_registration

    def extract_cars_links(self, src_code):
        # Extract cars links.
        cars_links = []

        a_tags = src_code.find_all("a", {"data-item-name": "detail-page-link"})

        for a_tag in a_tags:

            car_link = a_tag['href'].strip()
            cars_links.append(car_link)

        return cars_links
