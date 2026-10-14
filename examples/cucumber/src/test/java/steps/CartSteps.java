package steps;

import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.jupiter.api.Assertions;
import pages.InventoryPage;

/** Step definitions for cart.feature. Business language in, page-object calls out. */
public class CartSteps {

    private final InventoryPage inventory;

    // In a real suite the driver and pages arrive through dependency injection (e.g. PicoContainer).
    public CartSteps(InventoryPage inventory) {
        this.inventory = inventory;
    }

    @When("I add {string} to the cart")
    public void iAddToTheCart(String product) {
        inventory.addToCart(product);
    }

    @Then("the cart badge shows {int}")
    public void theCartBadgeShows(int expected) {
        Assertions.assertEquals(String.valueOf(expected), inventory.cartBadgeCount());
    }

    @And("the cart lists {string}")
    public void theCartLists(String product) {
        inventory.openCart();
        Assertions.assertEquals(product, inventory.firstCartItemName());
    }
}
