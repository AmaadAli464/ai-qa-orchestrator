Feature: Shopping cart
  As a shopper I can add an item to my cart so that I can buy it later.

  Background:
    Given I am logged in as a standard user

  Scenario: Adding an item updates the cart
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge shows 1
    And the cart lists "Sauce Labs Backpack"

  Scenario: A locked-out user cannot log in
    Given I am on the login page
    When I log in as the locked-out user
    Then I see the error "Sorry, this user has been locked out."
