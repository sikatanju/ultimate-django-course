from locust import HttpUser, task, between

from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)   
    
    # Adding weights
    @task(1)
    def view_products(self):
        print('View Products')
        collection_id = randint(2, 6)
        self.client.get(f'/store/products/?collection_id={collection_id}', name='/store/products')

    @task(1)
    def view_product_details(self):
        print('View Products Details')
        product_id = randint(1, 1000)
        self.client.get(f'/store/products/{product_id}', name='/store/products/:id')

    
    
    @task(1)
    def add_to_cart(self):
        print('Add to Cart')
        product_id = randint(1, 10)
        self.client.post(f'/store/carts/{self.cart_id}/items/', name='/store/carts/items/',
                            json={'product_id': product_id, 'quantity': 1})

    
    @task(10)
    def say_hello(self):
        self.client.get('/playground/hello/', name='/playground/hello/')


    def on_start(self) -> None:
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']