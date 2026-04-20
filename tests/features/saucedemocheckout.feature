Feature: SauceDemo checkout flow

  @regression
  Scenario: Complete checkout flow
    Given user is logged into saucedemo
    When user adds item to cart
    And user proceeds to checkout
    And user enters checkout details
    Then order should be successfully placed
