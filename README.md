Payment (Gateway) API v1
========================

This project implements v1 API for Payment Gateway (as a part of test assessment to apply for Software Engineer position
at [Coins.ph](https://coins.ph/)). You could find the full description of the task in [this file](https://drive.google.com/file/d/1qGMij-Nil1j0iw7khwjzpTmTl6mKlk47/view?usp=sharing).
Please, consider reading of the following parts if you want to know more on how it's working, how to run it locally,
how to contribute and how to deploy it.

Although it's proven to work system, there's still the big room for improvements. Next steps are described in `TODO`
section below. Those items should be adjusted as time goes on - having new experience in the domain and this particular
system.

Architecture
------------

The original requirements describe fine-grained and self-contained scope of business capabilities. So, **Microservice**
architecture pattern is the best fit for such independent system. That way let us follow SRP (Single Responsibility
Principle) - to have limited and focused business scope, helping to meet the agility in development and delivery of
services. This is the first iteration on Payment Gateway Microservice, taking all the original requirements as the
bounded context. Good news about Microservices is that we could just start with relatively broad service boundaries
and then refactor to smaller ones (as time goes on, business requirements are changing and we're getting more 
experience in this area).




How to Run and Use
------------------

### Run

Since all the things are wrapped with Docker - you could quickly start playing around with the system. Let's start from
the assumption that you've already cloned the repository to some location on your machine. First step will be to build
all the thing required for Payment (Gateway) API to run:

```bash
docker-compose up -d --build
```

At this point you will have all things ready for application to run. And as the next step you might want run the 
automated test suite to ensure that system works as expected:

```bash
docker-compose up payment.api.v1.autotests
```

To run the application, you should use the following command:

```bash
docker-compose up payment.api.v1
```

As you can see - all the services follow semantic naming. So it's pretty easy to start hacking around.

### Getting Started

To start working with the system you might need the following things:

##### 1. Run the application service

```bash
docker-compose up payment.api.v1.autotests
```

##### 2. Add sample data

You could do either from admin UI (accessing http://0.0.0.0:8000/admin) or using Django shell
(which is described below in [Django Shell](#django-shell--sample-data) section).

##### 3. Query API

Explore API: http://0.0.0.0/api

Explore API Documentation: http://0.0.0.0/docs

### Development

There're some commonly used flows during development. Let's see some examples.

#### Database Migration

First one is when you're making some changes in `models.py` (change in ORM code) and you want to reflect that change
in DB migration. So after you've changed the codebase you should generate migration and apply like follows:

```bash
docker-compose run payment.api.v1 python manage.py makemigrations
docker-compose up payment.api.v1.migrate
```

#### TDD

This project was implemented using TDD technique. That means that firstly we're writing a Test Case, describing how
some feature should operate. Then we're running test suite to ensure that it's failing. This is the good time to commit
this failing test in your working branch. As next step - you'll iterate (writing the code) to make that feature work
(proven by passing test suite). When test suite is passing - it's time to commit again.

Let me repeat myself to describe how you should run the automated test suite:

```bash
docker-compose up payment.api.v1.autotests
```

It's worth noting that even if you've changed some ORM code - there's no need to create migration before you will ensure
that feature (or bugfix) is working. Migrations are skipped during test run. So you should remember **to create migration(s)
and migrate when you have passing test suite**.

#### Celery Tasks

This project has just 1 Celery Task for now - the `process_payment` task, which purpose comes from it's name. But it's
very likely that we'll need more of them. At this point I would give advice about changes in Celery Tasks (edit existing
or create a new one). After you've made changes - you also have to restart Celery Worker(s) to let them get new code of
tasks. You could od that like follows:

```bash
docker-compose down
```

and then start all what you need, for example:

```bash
docker-compose up payment.api.v1
```

#### Django Shell (+ sample data)

Sometime you'll need to run Django Shell. You could do it like follows:

```bash
docker-compose run payment.api.v1 python manage.py shell
```

This is the good way to add some data for testing or development purpose. So you could import models and create some
instances:

```python
from payment_api_v1.models import Account, Balance, Payment

account1 = Account.objects.create(email='jerry@example.com')
account2 = Account.objects.create(email='tom@example.com')

account1_balance_usd = account1.create_balance('USD') 
account1_balance_php = account1.create_balance('PHP')

account2_balance_php = aacount2.create_balance('PHP')

from djmoney.money import Money

account1_balance_usd.money = Money(1000, 'USD')
account1_balance_usd.save()

account1_balance_php.money = Money(2000, 'PHP')
account1_balance_php.save()

payment = Payment.objects.create(balance_from=account2_balance_php, balance_to=account2_balance_php, money=Money(100, 'PHP'))
```

Contribution
------------

As a general rule of thumb:

1. Use git-flow and open pull request to merge any change in `staging`, `release-*` or `master` branch
2. Write tests first and ensure they pass before moving forward to QA stage
3. Use docstrings and type hinting to keep information about your code organized

All other pieces will placed in `CONTRIBUTING.md` file.

Deployment and Scalability
--------------------------



TODO
----

DevOps:

1. Add `healthcheck` parameter to all services in `docker-compose.yml` (where it's possible). That will help us to
catch the moment when a service is really up (not just container) - software inside that container should be ready
to operate.
2. Integrate `uWSGI` in the environment of application service.
3. Add `uWSGI Fast Router` to the list of services in Docker Compose file. Using subscription server we could make it
to act like a load balancer for application service nodes.
4. Add `Nginx` as a separate service. Make it to talk with `uWSGI Fast Router` load balancer, which will forward
requests to all the application nodes we have.
5. Think about decoupling `uWSGI Fast Router` and `Nginx` from this project and their usage for other Microservices.
6. Add application error-tracking system (e.g. Sentry) to start collecting reports about errors in the code. Integrate
codebase with it.
7. Integrate logs aggregator (e.g. Logstash + Kibana) to have one place to look for Nginx logs, uWSGI logs, Celery Logs,
etc ...
8. Since writes will appear more often than reads in the system - we should start from split of DB service into 2 parts - 
master and slave. Write to master, read from slave. Application should be also ready for this change.

Application:

1. Integrate authentication & authorization in the system (permissions? tokens? etc...). It should follow the same standard
as other microservices in the farm.
2. Moving automated test suite from pure Django to py.test will give us huge advantage. E.g., Celery has good set of
ready-to-use fixtures to run Celery Worker in a thread and so on.
3. Filter `Account` and `Balance` instances by `active` state. So, some of them may become disabled. That requires changes
on both ORM side and REST API side.
4. Add currency exchange capabilities, so transactions between balances with different currency will become possible.
5. Add capability to add custom currencies (e.g. new cryptocurrencies).
6. Avoid payments between same balance of same account. While payments between different balances of same
account sounds reasonable.

Documentation and Workflows:

1. Create `CONTRIBUTING.md` file in the root of this repository to store rules directly related
to contribution - Code of Conduct, Pull Requesting, etc ...