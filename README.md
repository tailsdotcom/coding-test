# Coding test for tails.com

## About this test

Think of this as an open source project. How would this have to look in order for you to be impressed with it, if you were to find it on GitHub? Now go and do that.

Please spend at least 90 minutes on this test. Feel free to take more time if you wish - make sure you are happy with your submission!

**Hint**: we are looking for a high-quality submission with great application architecture. Not a "get it done" approach. Stay away from frameworks and boilerplate code that handle everything for you. If you do use a framework, only use it as a thin layer, so we can see how you structure applications yourself.  

Remember that this test is your opportunity to show us how you think. Be clear about how you make decisions in your code, whether that is with comments, tests, or how you name things.

## What to do

Follow the three steps below to submit your coding test to us.

### First

* Create a Docker container with a new Python-based application. Any framework is fine, we prefer Flask.

### Second

#### If you are applying for a Backend Software Engineer role:
* Render the list of stores from the `stores.json` file in alphabetical order using a template.
* Use [Postcodes.io](https://postcodes.io) to get the latitude and longitude for each postcode. Render them next to each store location in the template.
* Build the functionality that allows you to return a list of stores in a given radius of a given postcode in the UK. The list must be ordered from north to south. No need to render anything, but the function needs to be unit tested.

#### If you are applying for a Full Stack Software Engineer role:
* Build an API that returns stores from the `stores.json` file, based on a given search string and unit test it. For example, return `"Newhaven"` when searching for `"hav"`. Make sure the search allows to use both city name and postcode.
* Order the results by matching postcode first and then matching city names. For example, `"br"` would have `"Orpington"` as the first result as its postcode is `"BR5 3RP"`. Next would be `"Bracknell"`, `"Broadstairs"`, `"Tunbridge_Wells"`, and `"Brentford"`
* Using your favourite frontend framework (we prefer Vue/React) on the user-facing side:
  * Build a frontend that renders a text field for the query and the list of stores that match it
  * Add suggestions to the query field as you type, with a debounce effect of 100ms and a minimum of 2 characters
  * Limit the results to 3 and lazy load the rest on page scroll

### Third

* Zip your code up and upload it to Greenhouse (our recruitment system). Use the link provided at the bottom of the email you received.
* Provide answers for the following questions with your submission:
  1. Which test did you complete? (backend or full-stack)
  2. If you had chosen to spend more time on this test, what would you have done differently?
  3. What part did you find the hardest? What part are you most proud of? In both cases, why?
  4. What is one thing we could do to improve this test?
