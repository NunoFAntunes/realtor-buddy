"""Main CLI entry point for Realtor Buddy."""

import click
import logging
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from ..utils.config import Config
from ..database.health_check import health_checker

console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.version_option(version='0.1.0')
def main(debug):
    """Realtor Buddy - Croatian Real Estate Property Search CLI."""
    if debug:
        Config.DEBUG = True
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")


@main.command()
def health():
    """Check database health and connectivity."""
    console.print("🏥 [bold blue]Checking database health...[/bold blue]")
    
    health_status = health_checker.comprehensive_health_check()
    
    # Display overall status
    status_color = {
        "healthy": "green",
        "warning": "yellow", 
        "unhealthy": "red",
        "error": "red"
    }.get(health_status["overall_status"], "white")
    
    console.print(f"\n📊 [bold]Overall Status:[/bold] [{status_color}]{health_status['overall_status'].upper()}[/{status_color}]")
    
    # Display connectivity details
    if "connectivity" in health_status:
        conn = health_status["connectivity"]
        conn_status = "✅" if conn.get("connected") else "❌"
        console.print(f"\n🔌 [bold]Database Connectivity:[/bold] {conn_status}")
        console.print(f"   Response Time: {conn.get('response_time_ms', 0):.2f}ms")
        
        if "error" in conn:
            console.print(f"   [red]Error: {conn['error']}[/red]")
    
    # Display table status
    if "table_status" in health_status:
        table = health_status["table_status"]
        table_status = "✅" if table.get("table_exists") else "❌"
        console.print(f"\n📋 [bold]Table Status:[/bold] {table_status}")
        
        if table.get("table_exists"):
            console.print(f"   Table: {table.get('table_name')}")
            console.print(f"   Columns: {table.get('column_count', 0)}")
            console.print(f"   Total Rows: {table.get('row_count', 0):,}")
        
        if "error" in table:
            console.print(f"   [red]Error: {table['error']}[/red]")
    
    # Display data quality
    if "data_quality" in health_status:
        quality = health_status["data_quality"]
        console.print(f"\n📈 [bold]Data Quality:[/bold]")
        
        if "quality_checks" in quality:
            quality_table = Table(show_header=True, header_style="bold magenta")
            quality_table.add_column("Check", style="cyan")
            quality_table.add_column("Status", justify="center")
            quality_table.add_column("Value", justify="right")
            quality_table.add_column("Description")
            
            for check in quality["quality_checks"]:
                status_icon = "✅" if check["status"] == "pass" else "⚠️"
                quality_table.add_row(
                    check["check"],
                    f"{status_icon} {check['status']}",
                    str(check["value"]),
                    check["description"]
                )
            
            console.print(quality_table)
        
        if "error" in quality:
            console.print(f"   [red]Error: {quality['error']}[/red]")
    
    console.print(f"\n🕐 [dim]Last checked: {health_status.get('timestamp', 'N/A')}[/dim]")


@main.command()
def config():
    """Show current configuration."""
    console.print("⚙️  [bold blue]Configuration Status[/bold blue]")
    
    # Validate configuration
    validation = Config.validate_config()
    
    # Display validation results
    if validation["valid"]:
        console.print("✅ [green]Configuration is valid[/green]")
    else:
        console.print("❌ [red]Configuration has issues[/red]")
        for issue in validation["issues"]:
            console.print(f"   [red]• {issue}[/red]")
    
    if validation["warnings"]:
        console.print("\n⚠️  [yellow]Configuration warnings:[/yellow]")
        for warning in validation["warnings"]:
            console.print(f"   [yellow]• {warning}[/yellow]")
    
    # Display key configuration values
    console.print("\n📋 [bold]Current Settings:[/bold]")
    
    config_table = Table(show_header=True, header_style="bold magenta")
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value")
    config_table.add_column("Source", style="dim")
    
    # Database settings
    config_table.add_row("DB_HOST", Config.DB_HOST, "Environment")
    config_table.add_row("DB_PORT", str(Config.DB_PORT), "Environment")
    config_table.add_row("DB_NAME", Config.DB_NAME, "Environment")
    config_table.add_row("DB_USER", Config.DB_USER, "Environment")
    
    # LLM settings
    config_table.add_row("LLM_PROVIDER", Config.LLM_PROVIDER, "Environment")
    config_table.add_row("LLM_MODEL", Config.LLM_MODEL, "Environment")
    config_table.add_row("LLM_TEMPERATURE", str(Config.LLM_TEMPERATURE), "Environment")
    
    # API Key status (don't show actual keys)
    openai_key_status = "✅ Set" if Config.OPENAI_API_KEY else "❌ Not set"
    anthropic_key_status = "✅ Set" if Config.ANTHROPIC_API_KEY else "❌ Not set"
    
    config_table.add_row("OPENAI_API_KEY", openai_key_status, "Environment")
    config_table.add_row("ANTHROPIC_API_KEY", anthropic_key_status, "Environment")
    
    # Application settings
    config_table.add_row("DEBUG", str(Config.DEBUG), "Environment")
    config_table.add_row("LOG_LEVEL", Config.LOG_LEVEL, "Environment")
    config_table.add_row("MAX_QUERY_RESULTS", str(Config.MAX_QUERY_RESULTS), "Environment")
    
    console.print(config_table)


@main.command()
@click.argument('query', required=False)
def search(query):
    """Search for properties using natural language."""
    if not query:
        console.print("❓ [yellow]No query provided. Property search functionality coming soon![/yellow]")
        console.print("\n🔮 [dim]Example queries you'll be able to use:[/dim]")
        console.print("   • Find apartments in Zagreb under 200,000 euros")
        console.print("   • Show me houses with sea view in Split")
        console.print("   • Properties with parking and elevator in city center")
        return
    
    console.print(f"🔍 [bold]Searching for:[/bold] {query}")
    console.print("🚧 [yellow]Property search functionality is under development![/yellow]")
    console.print("📝 [dim]This will be implemented in Phase 2 of the development plan.[/dim]")


if __name__ == '__main__':
    main()