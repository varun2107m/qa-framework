Feature: SauceDemo basic flows

  @smoke
  Scenario: Successful login
    Given user opens saucedemo login page
    When user logs in with "standard_user" and "secret_sauce"
    Then inventory page should be displayed

  @regression
  Scenario: Add item to cart
    Given user is logged into saucedemo
    When user adds item to cart
    Then item should be visible in cart



