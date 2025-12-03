#!/usr/bin/env python3
"""
Grocy Recipe Importer - Outil d'import automatique de recettes web vers Grocy
"""

import argparse
import sys
from pathlib import Path
from recipe_extractor import RecipeExtractor
from grocy_client import GrocyClient
from rich.console import Console
from rich.prompt import Confirm

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Importe des recettes depuis des sites web ou fichiers HTML vers Grocy"
    )
    parser.add_argument(
        "source",
        help="URL de la recette ou chemin vers un fichier HTML local"
    )
    parser.add_argument(
        "--grocy-url",
        required=True,
        help="URL de votre instance Grocy (ex: http://localhost:9283)"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Clé API Grocy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Affiche la recette sans l'importer dans Grocy"
    )
    
    args = parser.parse_args()
    
    try:
        # Étape 1 : Extraction de la recette
        console.print("[bold blue]🔍 Extraction de la recette...[/bold blue]")
        extractor = RecipeExtractor()
        recipe_data = extractor.extract(args.source)
        
        # Affichage de la recette extraite
        console.print(f"\n[bold green]✓ Recette extraite :[/bold green] {recipe_data['title']}")
        console.print(f"[dim]Portions:[/dim] {recipe_data.get('yields', 'N/A')}")
        console.print(f"[dim]Temps total:[/dim] {recipe_data.get('total_time', 'N/A')} min")
        console.print(f"\n[bold]Ingrédients ({len(recipe_data['ingredients'])}):[/bold]")
        for ing in recipe_data['ingredients'][:5]:  # Affiche les 5 premiers
            console.print(f"  • {ing}")
        if len(recipe_data['ingredients']) > 5:
            console.print(f"  ... et {len(recipe_data['ingredients']) - 5} autres")
        
        if args.dry_run:
            console.print("\n[yellow]Mode dry-run activé - Import annulé[/yellow]")
            return
        
        # Étape 2 : Connexion à Grocy
        console.print("\n[bold blue]🔗 Connexion à Grocy...[/bold blue]")
        grocy = GrocyClient(args.grocy_url, args.api_key)
        
        # Vérification de la connexion
        if not grocy.test_connection():
            console.print("[bold red]✗ Impossible de se connecter à Grocy[/bold red]")
            sys.exit(1)
        
        console.print("[green]✓ Connecté à Grocy[/green]")
        
        # Vérifier les unités disponibles
        units = grocy.get_quantity_units()
        if units:
            console.print(f"[dim]Unités disponibles: {len(units)} (utilisation de '{units[0]['name']}' par défaut)[/dim]")
        
        # Confirmation avant import
        if not Confirm.ask(f"\n[yellow]Importer '{recipe_data['title']}' dans Grocy ?[/yellow]"):
            console.print("[dim]Import annulé[/dim]")
            return
        
        # Étape 3 : Import dans Grocy
        console.print("\n[bold blue]📤 Import de la recette dans Grocy...[/bold blue]")
        recipe_id = grocy.import_recipe(recipe_data)
        
        console.print(f"[bold green]✓ Recette importée avec succès ![/bold green]")
        console.print(f"[dim]ID Grocy: {recipe_id}[/dim]")
        console.print(f"[dim]{len(recipe_data['ingredients'])} ingrédients ajoutés[/dim]")
        console.print(f"[dim]Accès: {args.grocy_url}/#recipe/{recipe_id}[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Erreur : {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()