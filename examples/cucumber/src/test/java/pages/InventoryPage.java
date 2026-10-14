package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** Page object for the inventory and cart. All locators live here, never in steps. */
public class InventoryPage {

    private final WebDriver driver;
    private final WebDriverWait wait;

    private static final By CART_BADGE = By.cssSelector(".shopping_cart_badge");
    private static final By CART_LINK = By.cssSelector(".shopping_cart_link");
    private static final By CART_ITEM_NAME = By.cssSelector(".inventory_item_name");

    public InventoryPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void addToCart(String productName) {
        String id = "add-to-cart-" + productName.toLowerCase().replace(' ', '-');
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("[data-test='" + id + "']"))).click();
    }

    public String cartBadgeCount() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(CART_BADGE)).getText();
    }

    public void openCart() {
        wait.until(ExpectedConditions.elementToBeClickable(CART_LINK)).click();
    }

    public String firstCartItemName() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(CART_ITEM_NAME)).getText();
    }
}
