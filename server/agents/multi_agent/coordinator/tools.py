def get_ulukulo_top_sales(month: int) -> dict:
    """
    Retrieves the top 3 sales items for a specified month at Ulukulo store.
    Provides detailed information about the top 3 best-selling products for each month
    from January to September 2025.

    Args:
        month (int): The target month to search. Must be an integer from 1 to 9
                    (corresponding to January through September 2025).

    Returns:
        dict: A dictionary containing sales information with the following properties:
            - status (str): Processing result status ("success" or "error")
            - month (str): Display format of the specified month (e.g., "2025年3月") or empty string on error
            - top_sales (list): List of top 3 sales items (empty list on error). Each element contains:
                - rank (int): Ranking position (1, 2, or 3)
                - product (str): Product name
                - sales (int): Sales amount in Japanese Yen
                - category (str): Product category
    """
    # 2025年1月から9月の固定データ
    sales_data = {
        1: [
            {
                "rank": 1,
                "product": "ヒートテックインナー",
                "sales": 1250000,
                "category": "インナーウェア",
            },
            {
                "rank": 2,
                "product": "ウルトラライトダウンジャケット",
                "sales": 980000,
                "category": "アウター",
            },
            {
                "rank": 3,
                "product": "ストレッチジーンズ",
                "sales": 850000,
                "category": "メンズウェア",
            },
        ],
        2: [
            {
                "rank": 1,
                "product": "カシミヤセーター",
                "sales": 1100000,
                "category": "レディースウェア",
            },
            {
                "rank": 2,
                "product": "フリースジャケット",
                "sales": 920000,
                "category": "アウター",
            },
            {
                "rank": 3,
                "product": "ヒートテックタイツ",
                "sales": 780000,
                "category": "インナーウェア",
            },
        ],
        3: [
            {
                "rank": 1,
                "product": "スプリングコート",
                "sales": 1350000,
                "category": "アウター",
            },
            {
                "rank": 2,
                "product": "コットンシャツ",
                "sales": 890000,
                "category": "メンズウェア",
            },
            {
                "rank": 3,
                "product": "レギンスパンツ",
                "sales": 750000,
                "category": "レディースウェア",
            },
        ],
        4: [
            {
                "rank": 1,
                "product": "UVカットカーディガン",
                "sales": 1180000,
                "category": "レディースウェア",
            },
            {
                "rank": 2,
                "product": "ポロシャツ",
                "sales": 950000,
                "category": "メンズウェア",
            },
            {
                "rank": 3,
                "product": "エアリズムTシャツ",
                "sales": 820000,
                "category": "インナーウェア",
            },
        ],
        5: [
            {
                "rank": 1,
                "product": "リネンブレンドシャツ",
                "sales": 1280000,
                "category": "メンズウェア",
            },
            {
                "rank": 2,
                "product": "ワイドパンツ",
                "sales": 1050000,
                "category": "レディースウェア",
            },
            {
                "rank": 3,
                "product": "サンダル",
                "sales": 680000,
                "category": "アクセサリー",
            },
        ],
        6: [
            {
                "rank": 1,
                "product": "エアリズムメッシュTシャツ",
                "sales": 1450000,
                "category": "インナーウェア",
            },
            {
                "rank": 2,
                "product": "ショートパンツ",
                "sales": 1120000,
                "category": "メンズウェア",
            },
            {
                "rank": 3,
                "product": "UVカット帽子",
                "sales": 790000,
                "category": "アクセサリー",
            },
        ],
        7: [
            {
                "rank": 1,
                "product": "ドライEXTシャツ",
                "sales": 1580000,
                "category": "スポーツウェア",
            },
            {
                "rank": 2,
                "product": "リラックスフィットパンツ",
                "sales": 1200000,
                "category": "メンズウェア",
            },
            {
                "rank": 3,
                "product": "エアリズムブラトップ",
                "sales": 950000,
                "category": "インナーウェア",
            },
        ],
        8: [
            {
                "rank": 1,
                "product": "感動ジャケット",
                "sales": 1650000,
                "category": "メンズウェア",
            },
            {
                "rank": 2,
                "product": "エアリズムワンピース",
                "sales": 1180000,
                "category": "レディースウェア",
            },
            {
                "rank": 3,
                "product": "ドライメッシュポロシャツ",
                "sales": 880000,
                "category": "スポーツウェア",
            },
        ],
        9: [
            {
                "rank": 1,
                "product": "秋色カーディガン",
                "sales": 1380000,
                "category": "レディースウェア",
            },
            {
                "rank": 2,
                "product": "フランネルシャツ",
                "sales": 1050000,
                "category": "メンズウェア",
            },
            {
                "rank": 3,
                "product": "ロングブーツ",
                "sales": 920000,
                "category": "アクセサリー",
            },
        ],
    }

    # 入力値の検証
    if not isinstance(month, int) or month < 1 or month > 9:
        return {
            "status": "error",
            "month": "",
            "top_sales": [],
        }

    # 指定された月のデータを取得
    top_sales = sales_data.get(month, [])

    return {
        "status": "success",
        "month": f"2025年{month}月",
        "top_sales": top_sales,
    }


def get_saizeriya_top_sales(month: int) -> dict:
    """
    Retrieves the top 3 sales menu items for a specified month at Saizeriya restaurant.
    Provides detailed information about the top 3 best-selling menu items for each month
    from January to September 2025.

    Args:
        month (int): The target month to search. Must be an integer from 1 to 9
                    (corresponding to January through September 2025).

    Returns:
        dict: A dictionary containing sales information with the following properties:
            - status (str): Processing result status ("success" or "error")
            - month (str): Display format of the specified month (e.g., "2025年3月") or empty string on error
            - top_sales (list): List of top 3 sales items (empty list on error). Each element contains:
                - rank (int): Ranking position (1, 2, or 3)
                - product (str): Menu item name
                - sales (int): Sales amount in Japanese Yen
                - category (str): Menu category
    """
    # 2025年1月から9月の固定データ（サイゼリ屋）
    sales_data = {
        1: [
            {
                "rank": 1,
                "product": "ミラノ風ドリア",
                "sales": 920000,
                "category": "ドリア",
            },
            {
                "rank": 2,
                "product": "ペペロンチーノ",
                "sales": 760000,
                "category": "パスタ",
            },
            {
                "rank": 3,
                "product": "マルゲリータピザ",
                "sales": 630000,
                "category": "ピザ",
            },
        ],
        2: [
            {
                "rank": 1,
                "product": "ミラノ風ドリア",
                "sales": 980000,
                "category": "ドリア",
            },
            {"rank": 2, "product": "辛味チキン", "sales": 710000, "category": "サイド"},
            {
                "rank": 3,
                "product": "小エビのサラダ",
                "sales": 650000,
                "category": "サラダ",
            },
        ],
        3: [
            {
                "rank": 1,
                "product": "たらこスパゲッティ",
                "sales": 870000,
                "category": "パスタ",
            },
            {
                "rank": 2,
                "product": "ミラノ風ドリア",
                "sales": 820000,
                "category": "ドリア",
            },
            {
                "rank": 3,
                "product": "マルゲリータピザ",
                "sales": 680000,
                "category": "ピザ",
            },
        ],
        4: [
            {
                "rank": 1,
                "product": "ペペロンチーノ",
                "sales": 910000,
                "category": "パスタ",
            },
            {
                "rank": 2,
                "product": "小エビのサラダ",
                "sales": 720000,
                "category": "サラダ",
            },
            {
                "rank": 3,
                "product": "ティラミス",
                "sales": 560000,
                "category": "デザート",
            },
        ],
        5: [
            {
                "rank": 1,
                "product": "冷製トマトパスタ",
                "sales": 940000,
                "category": "パスタ",
            },
            {
                "rank": 2,
                "product": "ミラノ風ドリア",
                "sales": 830000,
                "category": "ドリア",
            },
            {"rank": 3, "product": "辛味チキン", "sales": 700000, "category": "サイド"},
        ],
        6: [
            {
                "rank": 1,
                "product": "マルゲリータピザ",
                "sales": 960000,
                "category": "ピザ",
            },
            {
                "rank": 2,
                "product": "冷製トマトパスタ",
                "sales": 880000,
                "category": "パスタ",
            },
            {
                "rank": 3,
                "product": "ラムのグリル",
                "sales": 610000,
                "category": "グリル",
            },
        ],
        7: [
            {
                "rank": 1,
                "product": "冷製トマトパスタ",
                "sales": 1020000,
                "category": "パスタ",
            },
            {
                "rank": 2,
                "product": "ミラノ風ドリア",
                "sales": 840000,
                "category": "ドリア",
            },
            {"rank": 3, "product": "辛味チキン", "sales": 730000, "category": "サイド"},
        ],
        8: [
            {
                "rank": 1,
                "product": "ペペロンチーノ",
                "sales": 980000,
                "category": "パスタ",
            },
            {
                "rank": 2,
                "product": "マルゲリータピザ",
                "sales": 860000,
                "category": "ピザ",
            },
            {
                "rank": 3,
                "product": "プリンとティラミスの盛り合わせ",
                "sales": 640000,
                "category": "デザート",
            },
        ],
        9: [
            {
                "rank": 1,
                "product": "たらこスパゲッティ",
                "sales": 970000,
                "category": "パスタ",
            },
            {
                "rank": 2,
                "product": "ミラノ風ドリア",
                "sales": 900000,
                "category": "ドリア",
            },
            {
                "rank": 3,
                "product": "小エビのサラダ",
                "sales": 670000,
                "category": "サラダ",
            },
        ],
    }

    # 入力値の検証
    if not isinstance(month, int) or month < 1 or month > 9:
        return {
            "status": "error",
            "month": "",
            "top_sales": [],
        }

    # 指定された月のデータを取得
    top_sales = sales_data.get(month, [])

    return {
        "status": "success",
        "month": f"2025年{month}月",
        "top_sales": top_sales,
    }


def get_tofu_cinemas_schedule(month: int, day: int) -> dict:
    """
    Retrieves the movie screening schedule for TOFU Cinemas for a specified date.
    Returns a fixed schedule regardless of the input, while validating the inputs.

    Args:
        month (int): Month (1-12)
        day (int): Day (1-31)

    Returns:
        dict: A dictionary with following properties:
            - status (str): "success" or "error"
            - date (str): e.g., "2025年3月15日" or empty string on error
            - schedule (list): List of screenings. Each element contains:
                - screen (int): Screen number
                - title (str): Movie title
                - start_time (str): Start time in HH:MM
                - format (str): e.g., "2D", "3D"
    """
    if not isinstance(month, int) or not isinstance(day, int):
        return {"status": "error", "date": "", "schedule": []}

    if month < 1 or month > 12 or day < 1 or day > 31:
        return {"status": "error", "date": "", "schedule": []}

    fixed_schedule = [
        {"screen": 1, "title": "TOFU HEROES", "start_time": "10:00", "format": "2D"},
        {
            "screen": 2,
            "title": "豆腐探偵と秘密のレシピ",
            "start_time": "12:30",
            "format": "2D",
        },
        {
            "screen": 3,
            "title": "宇宙トーフの帰還",
            "start_time": "15:00",
            "format": "3D",
        },
        {
            "screen": 1,
            "title": "夜のトーフ・シネマティック",
            "start_time": "18:45",
            "format": "2D",
        },
        {"screen": 2, "title": "味噌の呼吸", "start_time": "21:15", "format": "2D"},
    ]

    return {
        "status": "success",
        "date": f"2025年{month}月{day}日",
        "schedule": fixed_schedule,
    }
