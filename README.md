Payment (Gateway) API v1
========================

This project implements v1 API for Payment Gateway (as a part of test assessment to apply for Software Engineer position
at [Coins.ph](https://coins.ph/)). You could find the full description of the task in [this file](https://drive.google.com/file/d/1qGMij-Nil1j0iw7khwjzpTmTl6mKlk47/view?usp=sharing).
Please, consider reading of the following parts if you want to know more on how it's working, how to run it locally,
how to contribute and how to deploy it.

Architecture
------------

The original requirements describe fine-grained and self-contained scope of business capabilities. So, **Microservice**
architecture pattern is the best fit for such independent system. That way let us follow SRP (Single Responsibility
Principle) - to have limited and focused business scope, helping to meet the agility in development and delivery of
services. This is the first iteration on Payment Gateway Microservice, taking all the original requirements as the
bounded context. Good news about Microservices is that we could just start with relatively broad service boundaries
and then refactor to smaller ones (as time goes on, business requirements are changing and we're getting more 
experience in this area).




How to Run
---------

Since all the things are wrapped with Docker - you could quickly start playing around with the system. Let's start from
the assumption that you've already cloned the repository to some location on your machine.



Contribution
------------


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