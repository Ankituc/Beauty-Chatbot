from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class UserQuery(BaseModel):
    product_type: str
    skin_type: str
    skin_problem: str


recommendation_data = {
    "moisturizer": {
        "dry": {
            "acne": "CeraVe Moisturizing Cream with salicylic acid.",
            "wrinkles": "Neutrogena Hydro Boost with Hyaluronic Acid.",
            "dullness": "Drunk Elephant Protini Polypeptide Cream.",
            "dark spots": "First Aid Beauty Ultra Repair Cream.",
            "redness": "Aveeno Calm + Restore Oat Gel."
        },
        "oily": {
            "acne": "La Roche-Posay Effaclar Mat.",
            "redness": "Paula's Choice Calm Redness Relief Moisturizer.",
            "blackheads": "COSRX Oil-Free Ultra-Moisturizing Lotion.",
            "dullness": "Clinique Dramatically Different Gel.",
            "pimples": "Clean & Clear Dual Action Moisturizer."
        },
        "combination": {
            "acne": "Neutrogena Oil-Free Moisturizer for Combination Skin.",
            "wrinkles": "Olay Luminous Whip Face Moisturizer SPF 25.",
            "redness": "La Roche-Posay Toleriane Double Repair.",
            "dullness": "Glow Recipe Watermelon Pink Juice Moisturizer."
        },
        "normal": {
            "dullness": "Embryolisse Lait-Crème Concentré.",
            "aging": "Clinique Smart Night Moisturizer.",
            "dark spots": "Murad Rapid Age Spot Correcting Cream."
        },
        "sensitive": {
            "acne": "Avene Tolerance Extreme Emulsion.",
            "redness": "La Roche-Posay Toleriane Ultra.",
            "wrinkles": "Cetaphil Rich Hydrating Cream."
        },
        "acne-prone": {
            "acne": "Cetaphil PRO Oil Absorbing Moisturizer.",
            "blackheads": "Bioderma Sebium Hydra.",
            "pimples": "Proactiv Green Tea Moisturizer."
        },
        "mature": {
            "wrinkles": "Olay Regenerist Micro-Sculpting Cream.",
            "aging": "L'Oreal Paris Age Perfect Cell Renewal.",
            "pigmentation": "StriVectin Advanced Retinol Intensive Night Moisturizer."
        }
    },
    "cleanser": {
        "oily": {
            "acne": "CeraVe Foaming Facial Cleanser.",
            "blackheads": "Bioré Deep Pore Charcoal Cleanser.",
            "dullness": "Youth To The People Superfood Cleanser."
        },
        "dry": {
            "dullness": "Fresh Soy Face Cleanser.",
            "redness": "Eucerin Advanced Cleansing Body & Face Cleanser."
        },
        "combination": {
            "pimples": "Neutrogena Oil-Free Acne Wash.",
            "blackheads": "Bioré Charcoal Acne Clearing Cleanser.",
            "acne": "La Roche-Posay Effaclar Purifying Foaming Gel."
        },
        "sensitive": {
            "acne": "Vanicream Gentle Facial Cleanser.",
            "redness": "Avene Extremely Gentle Cleanser Lotion.",
            "wrinkles": "Simple Kind to Skin Refreshing Facial Wash."
        },
        "acne-prone": {
            "acne": "PanOxyl Acne Foaming Wash 10% Benzoyl Peroxide.",
            "dark spots": "CeraVe Renewing SA Cleanser."
        }
    },
    "serum": {
        "normal": {
            "pigmentation": "TruSkin Vitamin C Serum.",
            "wrinkles": "Olay Regenerist Retinol 24 Night Serum.",
            "dullness": "The Ordinary Niacinamide 10% + Zinc 1%."
        },
        "sensitive": {
            "redness": "Dr. Jart+ Cicapair Tiger Grass Serum.",
            "dullness": "The Ordinary Azelaic Acid Suspension 10%.",
            "wrinkles": "The Inkey List Q10 Serum."
        },
        "oily": {
            "acne": "The Ordinary Salicylic Acid 2% Solution.",
            "blackheads": "Paula’s Choice BHA Liquid Exfoliant."
        },
        "dry": {
            "wrinkles": "Vichy LiftActiv Vitamin C Serum.",
            "dullness": "L'Oréal Revitalift Derm Intensives."
        },
        "mature": {
            "aging": "Estée Lauder Advanced Night Repair.",
            "wrinkles": "Skinceuticals C E Ferulic.",
            "dark spots": "Murad Rapid Dark Spot Correcting Serum."
        }
    },
    "sunscreen": {
        "oily": {
            "acne": "EltaMD UV Clear Broad-Spectrum SPF 46.",
            "dark spots": "Neutrogena Ultra Sheer Dry-Touch Sunscreen SPF 55."
        },
        "dry": {
            "wrinkles": "La Roche-Posay Anthelios Melt-in Milk Sunscreen SPF 60.",
            "redness": "Aveeno Positively Radiant Daily Moisturizer SPF 30."
        },
        "sensitive": {
            "redness": "Aveeno Positively Mineral Sensitive Skin Sunscreen.",
            "aging": "Blue Lizard Sensitive Mineral Sunscreen SPF 30."
        }
    },
    "toner": {
        "combination": {
            "acne": "Pixi Glow Tonic with Glycolic Acid.",
            "dullness": "The Ordinary Glycolic Acid 7% Toning Solution."
        },
        "normal": {
            "aging": "Kiehl's Calendula Herbal Extract Toner.",
            "pigmentation": "LANEIGE Cream Skin Toner & Moisturizer."
        },
        "dry": {
            "redness": "Thayers Alcohol-Free Rose Petal Witch Hazel.",
            "wrinkles": "Paula’s Choice Anti-Aging Resist Toner."
        },
        "oily": {
            "blackheads": "The Inkey List PHA Toner.",
            "acne": "COSRX AHA/BHA Clarifying Treatment Toner."
        }
    }
}


@app.get("/", response_class=HTMLResponse)
async def read_index():
    return FileResponse("static/index.html")

@app.post("/recommend")
async def recommend_product(query: UserQuery):
    try:
        recommendation = recommendation_data[query.product_type][query.skin_type][query.skin_problem]
        return JSONResponse(content={"recommendation": recommendation})
    except KeyError:
        return JSONResponse(content={"recommendation": "Sorry, no match found for that combination."})
