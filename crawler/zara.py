from playwright.sync_api import sync_playwright

def crawl_zara():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(
            "https://www.zara.com/kr/ko/woman-tshirts-l1362.html",
            wait_until="domcontentloaded",
            timeout=60000
        )

        # 쿠키 팝업
        try:
            page.click("button:has-text('모두 허용')", timeout=5000)
        except:
            pass

        # 상품 렌더링 대기
        page.wait_for_selector("article", timeout=20000)

        products = page.query_selector_all("article")
        print("상품 수:", len(products))

        for p in products[:5]:
            name_el = p.query_selector("h2")
            link_el = p.query_selector("a")

            name = name_el.inner_text() if name_el else "이름 없음"
            link = link_el.get_attribute("href") if link_el else ""

            print(name, link)

        browser.close()

if __name__ == "__main__":
    crawl_zara()
