# Configuration for scrapers
SCRAPER_CONFIGS = {
    "ALL_DOMAINS": ["forums", "jobs", "news", "reviews", "shopping"],

    "forums": {
        "BASE_URL": "https://www.tapuz.co.il/forums/",
        "RAW_OUTPUT_FILE": "../data/rawData/forums.csv",
        "TRANSFORMED_OUTPUT_FILE": "../data/transformed/transformed_forums_data.csv",
        "HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "validation": {
            "scraped": {
                "required_columns": ["Title","Topics", "Messages"]
                 },
            "transformed": {
                "required_columns": ["usersActiveGrade"],
            },
        },
    },

    "jobs": {
        "BASE_URL": "https://www.drushim.co.il/%D7%9E%D7%A9%D7%A8%D7%95%D7%AA-%D7%9C%D7%9C%D7%90-%D7%A7%D7%95%D7%A8%D7%95%D7%AA-%D7%97%D7%99%D7%99%D7%9D/?cv=1",
        "RAW_OUTPUT_FILE": "../data/rawData/jobs.csv",
        "TRANSFORMED_OUTPUT_FILE": "../data/transformed/transformed_jobs_data.csv",
        "HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "validation": {
            "scraped": {
                "required_columns": ["Title", "Company", "Location"],

            },
            "transformed": {
                "required_columns": ["job_name"],
            },
        },
    },

    "news": {
        "BASE_URL": "https://www.ynet.co.il/",
        "RAW_OUTPUT_FILE": "../data/rawData/news.csv",
        "TRANSFORMED_OUTPUT_FILE": "../data/transformed/transformed_news_data.csv",
        "HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "validation": {
            "scraped": {
                "required_columns": ["Header", "Summary", "DateTime"]
            },
            "transformed": {
                "required_columns": ["reading_time_segment"],
                "categorization": {
                    "reading_time_segment": ["Short", "Medium", "Long", "Very Long"],
                },
            },
        },
    },

    "reviews": {
        "BASE_URL": "https://www.seret.co.il/critics/moviecriticszone.asp",
        "RAW_OUTPUT_FILE": "../data/rawData/reviews.csv",
        "TRANSFORMED_OUTPUT_FILE": "../data/transformed/transformed_reviews_data.csv",
        "HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "validation": {
            "scraped": {
                "required_columns": ["Movie", "Review"],
                "non_empty_columns": ["Movie", "Review"],
            },
            "transformed": {
                "required_columns": ["user_feeling"],
                "categorization": {
                    "user_feeling": ["POSITIVE", "NEUTRAL", "NEGATIVE"],
                },
            },
        },
    },

    "shopping": {
        "BASE_URL": "https://lcp.co.il/",
        "RAW_OUTPUT_FILE": "../data/rawData/shopping.csv",
        "TRANSFORMED_OUTPUT_FILE": "../data/transformed/transformed_shopping_data.csv",
        "HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "validation": {
            "scraped": {
                "required_columns": ["Name", "Price", "Rating", "Categories"],
                "non_empty_columns": ["Name", "Price"],
            },
            "transformed": {
                "required_columns": ["Extracted_Product_Name", "Price_Category"],
                "categorization": {
                    "Price_Category": ["Low", "Medium", "High", "Premium"],
                },
            },
        },
    },
}
