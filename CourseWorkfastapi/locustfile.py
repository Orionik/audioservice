from locust import HttpUser, task, between

class Test(HttpUser):
    @task(3)
    def test(self):
        self.client.get("/user/")
        self.client.get("/singup/")


    @task
    def test1(self):
        self.client.get("/user/")
        self.client.post("/user/", data={"username":"123", "password":"123"})

    wait_time = between(0.5, 10)