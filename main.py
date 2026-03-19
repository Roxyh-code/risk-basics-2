from config import ASSETS, RECIPIENTS, EMAIL_SUBJECT, EXCEL_FILE, REPORT_DATE
from email_sender import send_email
from market_data import get_all_returns, generate_graphs, create_excel_report


def create_email_html(asset_returns):
    rows = []

    for asset_name, metrics in asset_returns.items():
        row = f"""
        <tr>
            <td>{asset_name}</td>
            <td>{metrics['YTD']:.2%}</td>
            <td>{metrics['MTD']:.2%}</td>
            <td>{metrics['DTD']:.2%}</td>
        </tr>
        """
        rows.append(row)

    rows_html = "\n".join(rows)

    html = f"""
    <html>
    <body style="font-family: Arial;">
        <h2>Daily Market Report</h2>
        <p><strong>Report Date:</strong> {REPORT_DATE}</p>
        <table border="1" cellpadding="8" cellspacing="0">
            <tr>
                <th>Asset</th>
                <th>YTD Return</th>
                <th>MTD Return</th>
                <th>DTD Return</th>
            </tr>
            {rows_html}
        </table>
    </body>
    </html>
    """
    return html


def main():
    asset_returns, data = get_all_returns()

    generate_graphs(data)
    create_excel_report(data)

    html = create_email_html(asset_returns)
    plot_files = [asset_config["plot_file"] for asset_config in ASSETS.values()]

    send_email(
        recipients=RECIPIENTS,
        subject=EMAIL_SUBJECT,
        content=html,
        attachments=[EXCEL_FILE],
        plots=plot_files
    )


if __name__ == "__main__":
    main()