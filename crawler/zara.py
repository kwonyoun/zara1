from playwright.sync_api import sync_playwright
import time

LIST_URL = "https://www.zara.com/kr/ko/woman-tshirts-l1362.html"


def log(msg):
    print(f"[LOG] {msg}")


def scroll_to_bottom(page, wait_selector):
    """
    상품이 더 이상 로딩되지 않을 때까지 스크롤
    """
    prev_count = 0

    while True:
        elements = page.query_selector_all(wait_selector)
        curr_count = len(elements)

        log(f"현재 로딩된 상품 수: {curr_count}")

        if curr_count == prev_count:
            log("더 이상 로딩 없음 → 스크롤 종료")
            break

        prev_count = curr_count
        page.mouse.wheel(0, 4000)
        time.sleep(1.5)


def crawl_zara_texts():
    log("크롤링 시작")

    texts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=80
        )

        context = browser.new_context(
            locale="ko-KR",
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        log("페이지 이동")
        page.goto(LIST_URL, wait_until="domcontentloaded", timeout=60000)

        # 쿠키
        try:
            page.click("button:has-text('모두 허용')", timeout=5000)
            log("쿠키 처리 완료")
        except:
            log("쿠키 없음")

        # ⭐ selector
        INFO_SELECTOR = ".product-grid-product-info__main-info h3"
        PRICE_SELECTOR = (
            ".product-grid-product-info__product-price "
            ".money-amount__main"
        )

        log("상품 최초 로딩 대기")
        page.wait_for_selector(INFO_SELECTOR, timeout=30000)

        # ✅ 여기서 전체 스크롤
        log("전체 상품 로딩을 위해 스크롤 시작")
        scroll_to_bottom(page, INFO_SELECTOR)

        ps = page.query_selector_all(INFO_SELECTOR)
        prices = page.query_selector_all(PRICE_SELECTOR)

        log(f"h3 태그 개수: {len(ps)}")
        log(f"가격 태그 개수: {len(prices)}")

        for i in range(min(len(ps), len(prices))):
            name = ps[i].inner_text().strip()
            price = prices[i].inner_text().strip()

            texts.append({
                "name": name,
                "price": price
            })

        browser.close()

    log(f"수집 완료: {len(texts)}개")
    return texts


def main():
    items = crawl_zara_texts()

    for i, item in enumerate(items, start=1):
        print(f"{i}. {item['name']} | {item['price']}")


if __name__ == "__main__":
    main()
