# Tails coding test

## About this task

Think of this as an open source project. How would this have to look like, in order for you to be impressed with it - if you were to find it on Github? Now go do that.

Try to limit the amount of time you spend on this to 90-120 minutes. However, feel free to spend more - just make sure you're happy with your submission!

_Hint_: we're looking for a high-quality submission with great application architecture, not a "just get it done"-like approach.

## What to do

### If you're applying for a backend role

* Create a new Python-based application (any framework is fine, we prefer Flask)
* Render the list of stores from the `stores.json` file in alphabetical order through a backend template
* Use postcodes.io to get the latitude and longitude for each postcode and render them next to each store location in the template
* Build the functionality that allows you to return a list of stores in any given radius of any given postcode in the UK ordered from north to south and unit test it - no need to render anything

### If you're applying for a full stack role

* Create a new backend application (any language is fine), using your favourite front-end framework (we'd prefer React, Vue or Ember though) on the user-facing side
* Build an API that returns stores from the `stores.json` file, based on a given search string in a performant way and unit test it, i.e. return "Newhaven" when searching for "hav" - make sure the search allows to use both city name and postcode
* Order the results by matching postcode first and then matching city names, i.e. "br" would have "Orpington" as the 1st result, "Bracknell" as the 2nd
* Build the frontend that renders the text field for the query and the list of stores that match it
* Add suggestions to the query field as you type, with a debounce effect of 100ms and a minimum of 2 characters
* Limit the results to 3 and lazy load the rest

### Finally

* Include and render your favourite gif at the top right-hand corner of your application
* Zip your code up and upload it into Greenhouse
* Tell us what test you completed (backend or full-stack)
* Tell us what you'd have changed if you'd have had more time?
* What bits did you find the toughest? What bit are you most proud of? In both cases, why?
* What's one thing we could do to improve this test?
