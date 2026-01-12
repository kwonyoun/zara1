from playwright.sync_api import sync_playwright
import time
import csv
import os

LIST_URL = "https://www.zara.com/kr/ko/woman-tshirts-l1362.html"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "zara_woman_tshirts.csv")


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

    items = []

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

        INFO_SELECTOR = ".product-grid-product-info__main-info h3"
        PRICE_SELECTOR = (
            ".product-grid-product-info__product-price "
            ".money-amount__main"
        )

        log("상품 최초 로딩 대기")
        page.wait_for_selector(INFO_SELECTOR, timeout=30000)

        log("전체 상품 로딩을 위해 스크롤 시작")
        scroll_to_bottom(page, INFO_SELECTOR)

        names = page.query_selector_all(INFO_SELECTOR)
        prices = page.query_selector_all(PRICE_SELECTOR)

        log(f"h3 태그 개수: {len(names)}")
        log(f"가격 태그 개수: {len(prices)}")

        for i in range(min(len(names), len(prices))):
            name = names[i].inner_text().strip().replace("\\", "")

            # 원본 가격 텍스트 (표시용)
            price_text = prices[i].inner_text().strip().replace("\\", "")

            # 숫자 가격 (DB/계산용)
            price = int(
                price_text
                .replace("₩", "")
                .replace(",", "")
                .strip()
            )

            items.append({
                "name": name,
                "price": price,
                "price_text": price_text
            })

        browser.close()

    log(f"수집 완료: {len(items)}개")
    return items


def save_to_csv(items):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "price", "price_text"]
        )
        writer.writeheader()
        writer.writerows(items)

    log(f"CSV 저장 완료 → {CSV_PATH}")


def main():
    items = crawl_zara_texts()
    save_to_csv(items)

    # 일부 출력 확인
    for i, item in enumerate(items[:20], start=1):
        print(f"{i}. {item['name']} | {item['price_text']} ({item['price']})")


if __name__ == "__main__":
    main()
