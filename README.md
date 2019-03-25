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




Local run
---------


Contribution
------------


Deployment
----------


TODO
----

