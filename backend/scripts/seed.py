import argparse
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.slugs import make_unique_slug, slugify
from app.db.session import create_db_engine, create_session_factory
from app.models.category import Category
from app.models.product import Product

# from app.models.photo import Photo

CATEGORIES_DATA = [
    {"name": "Кераміка", "is_visible": True, "sku_prefix": "CER"},
    {"name": "Текстиль", "is_visible": True, "sku_prefix": "TXT"},
    {"name": "Свічки", "is_visible": True, "sku_prefix": "CND"},
    {"name": "Кухня", "is_visible": True, "sku_prefix": "KTCH"},
    {"name": "Подарунки", "is_visible": True, "sku_prefix": "GFT"},
    {"name": "Прикраси", "is_visible": False, "sku_prefix": "JWL"},
]

RAW_PRODUCTS_DATA: list[dict[str, Any]] = [
    {
        "category": "Кераміка",
        "name": "Глечик ручної роботи, 1 л",
        "price": Decimal("780.00"),
        "stock": 5,
        "is_visible": True,
        "days_ago": 10,
        "short": "Традиційний глиняний глечик для молочних продуктів та напоїв.",
        "full": "Автентичний глечик, виготовлений вручну з екологічно чистої глини.",
    },
    {
        "category": "Кераміка",
        "name": "Керамічна чашка «Світанок», 350 мл",
        "price": Decimal("350.00"),
        "stock": 0,
        "is_visible": True,
        "days_ago": 5,
        "short": "Затишна керамічна чашка з м'яким градієнтним глазуруванням.",
        "full": ("Ідеальна чашка для кави чи чаю. Кожен екземпляр має унікальний візерунок."),
    },
    {
        "category": "Кераміка",
        "name": "Керамічна чашка «Карпати», 400 мл",
        "price": Decimal("380.50"),
        "stock": 2,
        "is_visible": True,
        "days_ago": 12,
        "short": "Велика чашка із зображенням гірських силуетів.",
        "full": "Ручна ліпка, текстурна глазур. Чудово утримує тепло напою.",
    },
    {
        "category": "Кераміка",
        "name": "Ваза «Дніпро», 30 см",
        "price": Decimal("1200.00"),
        "stock": 4,
        "is_visible": True,
        "days_ago": 40,
        "short": "Вишукана підлогова ваза з хвилястим рельєфом.",
        "full": ("Ваза підійде для сухоцвітів та живих квітів. Ручна робота майстрів."),
    },
    {
        "category": "Кераміка",
        "name": "Тарілка десертна «Хвиля»",
        "price": Decimal("290.00"),
        "stock": 10,
        "is_visible": True,
        "days_ago": 2,
        "short": "Керамічна тарілка діаметром 20 см.",
        "full": ("Пастельні тони та хвилясті краї роблять подачу десертів особливою."),
    },
    {
        "category": "Кераміка",
        "name": "Піала для супу «Озеро»",
        "price": Decimal("310.00"),
        "stock": 1,
        "is_visible": True,
        "days_ago": 25,
        "short": "Глибока керамічна піала, 500 мл.",
        "full": ("Підходить для перших страв, боулів та салатів. Стійка до гарячих температур."),
    },
    {
        "category": "Кераміка",
        "name": "Заварювальний чайник «Затишок»",
        "price": Decimal("950.00"),
        "stock": 3,
        "is_visible": True,
        "days_ago": 55,
        "short": "Об'ємний керамічний чайник із бамбуковою ручкою.",
        "full": "Вбудоване ситечко в носику утримує чаїнки. Ємність 800 мл.",
    },
    {
        "category": "Кераміка",
        "name": "Керамічна цукорниця «Гарбузик»",
        "price": Decimal("240.00"),
        "stock": 0,
        "is_visible": True,
        "days_ago": 70,
        "short": "Симпатична цукорниця з кришечкою.",
        "full": "Виконана у формі невеликого гарбуза. Прикрасить будь-який стіл.",
    },
    {
        "category": "Кераміка",
        "name": "Маслянка керамічна «Млин»",
        "price": Decimal("420.00"),
        "stock": 6,
        "is_visible": True,
        "days_ago": 15,
        "short": "Зручна маслянка з високою кришкою.",
        "full": ("Зберігає вершкове масло свіжим та м'яким без сторонніх запахів."),
    },
    {
        "category": "Кераміка",
        "name": "Підсвічник керамічний «Вежа»",
        "price": Decimal("190.00"),
        "stock": 8,
        "is_visible": False,
        "days_ago": 80,
        "short": "Лаконічний підсвічник для стандартних свічок.",
        "full": "Матова кераміка чорного кольору.",
    },
    {
        "category": "Кераміка",
        "name": "Керамічне кашпо «Еко»",
        "price": Decimal("460.00"),
        "stock": 7,
        "is_visible": True,
        "days_ago": 4,
        "short": "Кашпо для хатніх рослин з дренажним отвором.",
        "full": "Натуральна текстура без покриття яскравішою глазур'ю.",
    },
    {
        "category": "Кераміка",
        "name": "Набір керамічних солонки та перечниці",
        "price": Decimal("280.00"),
        "stock": 12,
        "is_visible": True,
        "days_ago": 60,
        "short": "Компактні ємності для спецій.",
        "full": "Зручні силіконові заглушки знизу для легкого заповнення.",
    },
    {
        "category": "Кераміка",
        "name": "Аромалампа керамічна «Місяць»",
        "price": Decimal("330.00"),
        "stock": 2,
        "is_visible": True,
        "days_ago": 35,
        "short": "Аромалампа для ефірних олій.",
        "full": ("Вирізаний орнамент створює гарні тіні при горінні чайної свічки."),
    },
    {
        "category": "Текстиль",
        "name": "Лляна скатертина «Етно», 150х220 см",
        "price": Decimal("1450.00"),
        "stock": 5,
        "is_visible": True,
        "days_ago": 8,
        "short": "100% натуральний льон із вишитим орнаментом.",
        "full": ("Святкова скатертина, що надасть інтер'єру особливого українського колориту."),
    },
    {
        "category": "Текстиль",
        "name": "Набір лляних серветок (4 шт.)",
        "price": Decimal("520.00"),
        "stock": 15,
        "is_visible": True,
        "days_ago": 20,
        "short": "Столові серветки 40х40 см з натурального льону.",
        "full": "М'які, приємні на дотик та легко перуться.",
    },
    {
        "category": "Текстиль",
        "name": "Декоративна подушка «Опішня»",
        "price": Decimal("680.00"),
        "stock": 4,
        "is_visible": True,
        "days_ago": 45,
        "short": "Подушка з авторським геометричним принтом.",
        "full": ("Знімний чохол на блискавці. Наповнювач — гіпоалергенний холофайбер."),
    },
    {
        "category": "Текстиль",
        "name": "Плед вовняний «Затишок», 140х200 см",
        "price": Decimal("1890.00"),
        "stock": 3,
        "is_visible": True,
        "days_ago": 18,
        "short": "Теплий плед із натуральної овечої вовни.",
        "full": "Класичний карпатський плед у клітинку. Дуже теплий та м'який.",
    },
    {
        "category": "Текстиль",
        "name": "Кухонний фартух «Майстер»",
        "price": Decimal("410.00"),
        "stock": 10,
        "is_visible": True,
        "days_ago": 50,
        "short": "Щільний бавовняний фартух із великою кишенею.",
        "full": "Регульований шийний ремінець. Захищає одяг під час готування.",
    },
    {
        "category": "Текстиль",
        "name": "Набір кухонних рушників (3 шт.)",
        "price": Decimal("360.00"),
        "stock": 20,
        "days_ago": 65,
        "is_visible": True,
        "short": "Вафельні рушники з 100% бавовни.",
        "full": "Чудово вбирають вологу та швидко сохнуть.",
    },
    {
        "category": "Текстиль",
        "name": "Тканина кухонна декоративна «Ранчо»",
        "price": Decimal("180.00"),
        "stock": 0,
        "is_visible": False,
        "days_ago": 85,
        "short": "Раннер на стіл 40х140 см.",
        "full": "Створює акцент у центрі обіднього столу.",
    },
    {
        "category": "Текстиль",
        "name": "Лляний мішечок для хліба",
        "price": Decimal("150.00"),
        "stock": 8,
        "is_visible": True,
        "days_ago": 30,
        "short": "Екологічна упаковка для зберігання випічки.",
        "full": "Дозволяє хлібу дихати та довше залишатися свіжим.",
    },
    {
        "category": "Текстиль",
        "name": "Прикапка для гарячого (2 шт.)",
        "price": Decimal("220.00"),
        "stock": 14,
        "is_visible": True,
        "days_ago": 75,
        "short": "Щільні термостійкі прихватки.",
        "full": "Зручні петлі для підвішування.",
    },
    {
        "category": "Свічки",
        "name": "Свічка соєва «Липа»",
        "price": Decimal("450.00"),
        "stock": 6,
        "is_visible": True,
        "days_ago": 3,
        "short": "Ароматична свічка у скляній баночці з соєвого воску.",
        "full": ("Ніжний аромат солодкого цвіту липи. Час горіння до 40 годин."),
    },
    {
        "category": "Свічки",
        "name": "Свічка з вощини «Медовий аромат»",
        "price": Decimal("120.00"),
        "stock": 25,
        "is_visible": True,
        "days_ago": 14,
        "short": "Натуральна свічка з 100% бджолиного воску.",
        "full": ("При горінні виділяє корисні фітонциди та легкий медовий аромат."),
    },
    {
        "category": "Свічки",
        "name": "Свічка соєва «Хвойний ліс»",
        "price": Decimal("480.00"),
        "stock": 3,
        "is_visible": True,
        "days_ago": 22,
        "short": "Свічка з дерев'яним ґнотом, що потріскує.",
        "full": "Аромат сосни, кедра та свіжої хвої.",
    },
    {
        "category": "Свічки",
        "name": "Набір столових свічок (6 шт.)",
        "price": Decimal("390.00"),
        "stock": 11,
        "is_visible": True,
        "days_ago": 40,
        "short": "Конусоподібні свічки без аромату.",
        "full": "Висота 25 см. Час горіння однієї свічки — 7 годин.",
    },
    {
        "category": "Свічки",
        "name": "Свічка у керамічній піалі «Лаванда»",
        "price": Decimal("550.10"),
        "stock": 4,
        "is_visible": True,
        "days_ago": 28,
        "short": "Соєва свічка в кераміці ручної роботи.",
        "full": ("Після вигоряння воску ємність можна використовувати як піалу."),
    },
    {
        "category": "Свічки",
        "name": "Свічка масажна «Ваніль та Кокос»",
        "price": Decimal("520.00"),
        "stock": 7,
        "is_visible": True,
        "days_ago": 52,
        "short": "Свічка з натуральними оліями для догляду за шкірою.",
        "full": "Розплавлений віск використовується як тепла масажна олія.",
    },
    {
        "category": "Свічки",
        "name": "Свічка насипна пальмова",
        "price": Decimal("260.00"),
        "stock": 1,
        "is_visible": True,
        "days_ago": 68,
        "short": "Гранульований віск у комплекті з ґнотом.",
        "full": "Створює ефект кристалічного візерунка при застиганні.",
    },
    {
        "category": "Свічки",
        "name": "Свічка декоративна «Сфера»",
        "price": Decimal("310.00"),
        "stock": 0,
        "is_visible": False,
        "days_ago": 88,
        "short": "Куляста свічка бежевого кольору.",
        "full": "Ідеальний елемент декору для зйомок чи інтер'єру.",
    },
    {
        "category": "Кухня",
        "name": "Дошка для нарізання «Дубова класика»",
        "price": Decimal("890.00"),
        "stock": 8,
        "is_visible": True,
        "days_ago": 7,
        "short": "Масивна торцева дошка з дуба.",
        "full": ("Оброблена мінеральним маслом та бджолиним воском. Не затуплює ножі."),
    },
    {
        "category": "Кухня",
        "name": "Лопатка дерев'яна з черешні",
        "price": Decimal("110.00"),
        "stock": 30,
        "is_visible": True,
        "days_ago": 11,
        "short": "Екологічний кухонний прибор.",
        "full": "Безпечна для посуду з антипригарним покриттям.",
    },
    {
        "category": "Кухня",
        "name": "Качалка для тіла з орнаментом",
        "price": Decimal("340.00"),
        "stock": 5,
        "is_visible": True,
        "days_ago": 33,
        "short": "Фактурна качалка для візерункового печива.",
        "full": "Залишає чіткий красивий відбиток на тісті.",
    },
    {
        "category": "Кухня",
        "name": "Ступка з макітрою та товкачиком",
        "price": Decimal("640.25"),
        "stock": 3,
        "is_visible": True,
        "days_ago": 48,
        "short": "Глиняна макітра для перетирання маку та спецій.",
        "full": ("Традиційний український кухонний посуд з шорсткою внутрішньою поверхнею."),
    },
    {
        "category": "Кухня",
        "name": "Підставка під гаряче з дуба",
        "price": Decimal("230.00"),
        "stock": 18,
        "is_visible": True,
        "days_ago": 19,
        "short": "Надійна дерев'яна підставка.",
        "full": "Захищає стільницю від високих температур.",
    },
    {
        "category": "Кухня",
        "name": "Підставка для кухонних приборів",
        "price": Decimal("370.00"),
        "stock": 9,
        "is_visible": True,
        "days_ago": 58,
        "short": "Органайзер з дерева та кераміки.",
        "full": "Зручно зберігати лопатки, вінчики та ложки.",
    },
    {
        "category": "Кухня",
        "name": "Хлібниця дерев'яна «Сканди»",
        "price": Decimal("1150.00"),
        "stock": 2,
        "is_visible": True,
        "days_ago": 72,
        "short": "Хлібниця зі зсувною кришкою.",
        "full": "Зберігає хлібобулочні вироби свіжими.",
    },
    {
        "category": "Кухня",
        "name": "Форма для випікання глиняна",
        "price": Decimal("750.00"),
        "stock": 4,
        "is_visible": True,
        "days_ago": 82,
        "short": "Екологічна форма для запікання м'яса та овочів.",
        "full": "Запечені страви виходять особливо соковитими.",
    },
    {
        "category": "Кухня",
        "name": "Ложка дерев'яна велика",
        "price": Decimal("95.00"),
        "stock": 22,
        "is_visible": False,
        "days_ago": 89,
        "short": "Ложка для розливання та перемішування.",
        "full": "Ручна вирізка з липи.",
    },
    {
        "category": "Подарунки",
        "name": "Подарунковий набір «Затишний вечір»",
        "price": Decimal("1290.00"),
        "stock": 7,
        "is_visible": True,
        "days_ago": 1,
        "short": "Набір: чашка, соєва свічка та крафтовий чай.",
        "full": ("Упакований у стильну крафтову коробку зі стрічкою та листівкою."),
    },
    {
        "category": "Подарунки",
        "name": "Подарунковий сертифікат 1000 ₴",
        "price": Decimal("1000.00"),
        "stock": 99,
        "is_visible": True,
        "days_ago": 16,
        "short": "Електронний або друкований сертифікат.",
        "full": "Дійсний протягом 1 року на весь асортимент магазину.",
    },
    {
        "category": "Подарунки",
        "name": "Набір крафтового меду (3 банки)",
        "price": Decimal("495.75"),
        "stock": 12,
        "is_visible": True,
        "days_ago": 24,
        "short": "Мед із різнотрав'я, акації та горішками.",
        "full": "3 скляні баночки по 150 г у дерев'яному боксі.",
    },
    {
        "category": "Подарунки",
        "name": "Крафтовий чайний набір «Карпатські трави»",
        "price": Decimal("320.00"),
        "stock": 15,
        "is_visible": True,
        "days_ago": 38,
        "short": "Збір запашних гірських трав.",
        "full": "Чебрець, м'ята, Іван-чай та ягоди шипшини.",
    },
    {
        "category": "Подарунки",
        "name": "Комплект листівка + підставка під чашку",
        "price": Decimal("130.00"),
        "stock": 40,
        "is_visible": True,
        "days_ago": 42,
        "short": "Милий дрібний подарунок.",
        "full": ("Авторська ілюстрація на цупкому папері та костери з коркового дерева."),
    },
    {
        "category": "Подарунки",
        "name": "Набір керамічних костерів (4 шт.)",
        "price": Decimal("380.00"),
        "stock": 6,
        "is_visible": True,
        "days_ago": 59,
        "short": "Підставки під гарячі чашки з розписом.",
        "full": "Захищають меблі від плям та подряпин.",
    },
    {
        "category": "Подарунки",
        "name": "Подарунковий бокс «Українські традиції»",
        "price": Decimal("1650.00"),
        "stock": 2,
        "is_visible": True,
        "days_ago": 77,
        "short": ("Ексклюзивний набір із вишитою серветкою та глиняним кубком."),
        "full": "Прекрасний сувенір для друзів чи іноземних гостей.",
    },
    {
        "category": "Подарунки",
        "name": "Шоколад крафтовий з сушеними ягодами",
        "price": Decimal("170.00"),
        "stock": 18,
        "is_visible": True,
        "days_ago": 86,
        "short": "Чорний шоколад 70% з журавлиною та фундуком.",
        "full": ("Натуральні інгредієнти без додавання штучних ароматизаторів."),
    },
]


def seed_data(session: Session, reset: bool = False) -> dict[str, int]:
    existing_categories_count = session.query(Category).count()
    if existing_categories_count > 0 and not reset:
        print(
            "Categories already exist. Execution stopped. "
            "Use --reset to delete all photos, products, and categories first."
        )
        return {"categories": 0, "products": 0}

    if reset:
        # session.execute(delete(Photo))
        session.execute(delete(Product))
        session.execute(delete(Category))
        session.commit()

    categories_map: dict[str, Category] = {}
    created_categories_count = 0

    for index, cat_info in enumerate(CATEGORIES_DATA, start=1):
        cat_slug = make_unique_slug(
            slugify(cat_info["name"]),
            lambda s: session.query(Category).filter_by(slug=s).first() is not None,
        )
        category = Category(
            name=cat_info["name"],
            slug=cat_slug,
            is_visible=cat_info["is_visible"],
            position=index,
        )
        session.add(category)
        session.flush()
        categories_map[cat_info["name"]] = category
        created_categories_count += 1

    created_products_count = 0
    sku_counters: dict[str, int] = {}
    now = datetime.now(UTC)

    for prod_info in RAW_PRODUCTS_DATA:
        cat_name = prod_info["category"]
        category = categories_map[cat_name]

        prefix = next(c["sku_prefix"] for c in CATEGORIES_DATA if c["name"] == cat_name)
        sku_counters.setdefault(prefix, 1)
        sku = f"{prefix}-{sku_counters[prefix]:04d}"
        sku_counters[prefix] += 1

        base_slug = slugify(prod_info["name"])
        prod_slug = make_unique_slug(
            base_slug,
            lambda s: session.query(Product).filter_by(slug=s).first() is not None,
        )

        created_at = now - timedelta(days=prod_info["days_ago"])

        product = Product(
            name=prod_info["name"],
            slug=prod_slug,
            sku=sku,
            price=prod_info["price"],
            stock=prod_info["stock"],
            is_visible=prod_info["is_visible"],
            short_description=prod_info["short"],
            description=prod_info["full"],
            category_id=category.id,
            created_at=created_at,
        )
        session.add(product)
        created_products_count += 1

    session.commit()

    summary = {
        "categories": created_categories_count,
        "products": created_products_count,
    }
    print(f"Created {created_categories_count} categories and {created_products_count} products.")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed database with sample data.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset existing data before seeding",
    )
    args = parser.parse_args()

    settings = Settings()
    engine = create_db_engine(settings)
    SessionLocal = create_session_factory(engine)

    with SessionLocal() as session:
        summary = seed_data(session, reset=args.reset)
        print(
            f"Seeding completed: {summary['categories']} categories,"
            f" {summary['products']} products created."
        )


if __name__ == "__main__":
    main()
