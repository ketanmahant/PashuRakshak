from django.core.management.base import BaseCommand
from diagnosis.models import Disease


PROTOTYPE_DISEASES = [
    {
        "name": "Foot and Mouth Disease (FMD)",
        "description": "A severe, highly contagious viral disease of cloven-hoofed animals causing painful blister-like lesions on the tongue, gums, teats, and interdigital spaces of the feet.",
        "animal_types": ["cow", "buffalo", "sheep", "goat", "pig"],
        "symptoms": {
            "fever": 2,
            "excessive salivation": 3,
            "mouth lesions": 3,
            "lameness": 2,
            "loss of appetite": 1,
            "reduced milk production": 2,
        },
        "risk_level": "HIGH",
        "recommended_action": "Quarantine the affected animal immediately to prevent spread. Do not move livestock. Disinfect sheds and footwear. Contact a qualified veterinarian for symptomatic care and notify local authorities.",
    },
    {
        "name": "Lumpy Skin Disease",
        "description": "A viral disease of cattle and water buffalo transmitted by biting insects, characterized by distinctive firm, raised nodules throughout the skin and mucous membranes.",
        "animal_types": ["cow", "buffalo"],
        "symptoms": {
            "fever": 1,
            "skin nodules": 3,
            "swelling": 2,
            "loss of appetite": 1,
            "nasal discharge": 1,
            "reduced milk production": 2,
        },
        "risk_level": "HIGH",
        "recommended_action": "Isolate the animal in a vector-screened area. Control flies, mosquitoes, and ticks around the shelter. Provide clean drinking water and contact a qualified veterinarian for supportive therapy.",
    },
    {
        "name": "Hemorrhagic Septicemia (HS)",
        "description": "An acute, fatal bacterial septicemia primarily affecting cattle and water buffalo, causing severe inflammatory edema in the throat region and rapid asphyxiation.",
        "animal_types": ["cow", "buffalo"],
        "symptoms": {
            "fever": 2,
            "difficulty breathing": 3,
            "swelling": 3,
            "excessive salivation": 2,
            "weakness": 2,
            "sudden death": 3,
        },
        "risk_level": "CRITICAL",
        "recommended_action": "EMERGENCY: Immediate veterinary intervention is critical within the first hours. Administer prescription antibiotics under veterinary supervision before endotoxemia advances.",
    },
    {
        "name": "Peste des Petits Ruminants (PPR)",
        "description": "Also known as goat plague or ovine rinderpest, a highly infectious viral disease of goats and sheep causing acute necrotizing stomatitis, purulent ocular discharges, and severe enteritis.",
        "animal_types": ["goat", "sheep"],
        "symptoms": {
            "fever": 2,
            "mouth lesions": 3,
            "nasal discharge": 2,
            "eye discharge": 2,
            "diarrhea": 3,
            "difficulty breathing": 2,
            "loss of appetite": 1,
        },
        "risk_level": "HIGH",
        "recommended_action": "Strictly isolate affected small ruminants. Provide soft, non-abrasive feed and oral rehydration therapy. Request veterinary assistance for supportive therapy and vaccination of healthy flock members.",
    },
    {
        "name": "Anthrax",
        "description": "A peracute, rapidly lethal zoonotic infection caused by Bacillus anthracis. Characterized by sudden collapse, rapid bloat, and dark unclotted blood escaping from body orifices.",
        "animal_types": ["cow", "buffalo", "sheep", "goat"],
        "symptoms": {
            "sudden death": 3,
            "bleeding": 3,
            "bloody stool": 3,
            "fever": 2,
            "difficulty breathing": 2,
            "weakness": 2,
        },
        "risk_level": "CRITICAL",
        "recommended_action": "CRITICAL DANGER (ZOONOSIS): DO NOT OPEN OR SKIN THE CARCASS. Avoid any direct human contact. Immediately notify local animal health authorities for biosecure burial/cremation and ring vaccination.",
    },
    {
        "name": "Mastitis",
        "description": "Inflammation of the mammary gland/udder, typically caused by bacterial entry through the teat canal, leading to swollen, hard quarters and abnormal milk (clots, flakes, or watery).",
        "animal_types": ["cow", "buffalo", "goat", "sheep"],
        "symptoms": {
            "swelling": 3,
            "reduced milk production": 3,
            "fever": 1,
            "loss of appetite": 1,
            "weakness": 1,
        },
        "risk_level": "MEDIUM",
        "recommended_action": "Stop milking into the general milk supply. Milk out the affected quarter frequently and discard milk safely. Have a qualified veterinarian perform a California Mastitis Test (CMT) and prescribe intramammary therapy.",
    },
    {
        "name": "Black Quarter (BQ)",
        "description": "An acute, soil-borne clostridial infection in ruminants, causing crepitant (crackling) gangrenous swellings in the heavy musculature of shoulders or hindquarters, followed by severe lameness.",
        "animal_types": ["cow", "buffalo", "sheep"],
        "symptoms": {
            "lameness": 3,
            "swelling": 3,
            "fever": 2,
            "loss of appetite": 1,
            "weakness": 2,
            "sudden death": 2,
        },
        "risk_level": "CRITICAL",
        "recommended_action": "URGENT: Call a veterinarian immediately. High-dose penicillin treatment may be effective only in very early stages. Isolate carcass safely and vaccinate herd against Clostridium chauvoei.",
    },
    {
        "name": "Sheep and Goat Pox",
        "description": "A contagious capripoxvirus disease of small ruminants causing fever, followed by characteristic papules, nodules, and necrotic scabs on hairless skin and lungs.",
        "animal_types": ["sheep", "goat"],
        "symptoms": {
            "fever": 2,
            "skin lesions": 3,
            "skin nodules": 2,
            "nasal discharge": 2,
            "difficulty breathing": 1,
            "loss of appetite": 1,
        },
        "risk_level": "HIGH",
        "recommended_action": "Isolate all affected animals. Treat secondary skin infections with topical antiseptics under veterinary advice. Disinfect all pens and feed troughs.",
    },
    {
        "name": "Classical Swine Fever (Hog Cholera)",
        "description": "A highly contagious viral disease of pigs causing high body temperature, hemorrhages in skin, lethargy, vomiting, and yellowish diarrhea.",
        "animal_types": ["pig"],
        "symptoms": {
            "fever": 2,
            "skin lesions": 2,
            "diarrhea": 2,
            "vomiting": 2,
            "weakness": 2,
            "coughing": 1,
            "sudden death": 2,
        },
        "risk_level": "HIGH",
        "recommended_action": "Strict quarantine of swine housing. Prohibit pig movement and swill feeding. Contact state veterinary services immediately for confirmatory diagnosis.",
    },
    {
        "name": "Avian Influenza (Bird Flu)",
        "description": "A contagious viral disease of poultry capable of causing severe respiratory distress, cyanosis of wattles/comb, facial edema, and high sudden mortality.",
        "animal_types": ["poultry"],
        "symptoms": {
            "sudden death": 3,
            "difficulty breathing": 2,
            "swelling": 2,
            "nasal discharge": 2,
            "diarrhea": 2,
            "loss of appetite": 2,
            "reduced milk production": 1,
        },
        "risk_level": "CRITICAL",
        "recommended_action": "CRITICAL BIOSECURITY: Isolate the poultry shed immediately. Wear masks and protective gloves. Report immediately to government animal husbandry officers.",
    },
]


class Command(BaseCommand):
    help = "Seed prototype livestock disease knowledge base"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in PROTOTYPE_DISEASES:
            disease, created = Disease.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "animal_types": item["animal_types"],
                    "symptoms": item["symptoms"],
                    "risk_level": item["risk_level"],
                    "recommended_action": item["recommended_action"],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded disease knowledge base! Created: {created_count}, Updated: {updated_count}"
            )
        )
