from flask import Flask, render_template, request, redirect, url_for
import store

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("customers"))


@app.route("/customers")
def customers():
    accounts = store.load_accounts()
    opportunities = store.load_opportunities()
    # Only show top-level accounts (not subsidiaries)
    top_level = [a for a in accounts if not a.parent_id]
    top_level.sort(key=lambda a: a.name)

    customers = []
    for account in top_level:
        account_opps = [o for o in opportunities if o.account_id == account.id]
        health = store.calculate_health_score(account, account_opps)
        customers.append((account, health))

    # Sort: scored customers by health (worst first), then prospects at bottom
    def sort_key(pair):
        account, health = pair
        if health is None:
            return (1, 0)  # prospects go last
        return (0, health.score)

    customers.sort(key=sort_key)

    return render_template("customers.html", customers=customers)


@app.route("/alerts")
def alerts():
    alert_list = store.get_all_alerts()
    total_arr_at_risk = sum(a.arr for a in alert_list)
    return render_template("alerts.html", alerts=alert_list, total_arr_at_risk=total_arr_at_risk)


@app.route("/source-data")
def source_data():
    accounts = store.load_accounts()
    contacts = store.load_contacts()
    opportunities = store.load_opportunities()
    companies = store.load_companies()
    accounts.sort(key=lambda a: a.name)
    contacts.sort(key=lambda c: (c.last_name, c.first_name))
    opportunities.sort(key=lambda o: o.name)
    companies.sort(key=lambda c: c.company_name)
    return render_template("source_data.html",
                         accounts=accounts,
                         contacts=contacts,
                         opportunities=opportunities,
                         companies=companies)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = []
    if query:
        accounts = store.search_accounts(query)
        opportunities = store.load_opportunities()
        for account in accounts:
            account_opps = [o for o in opportunities if o.account_id == account.id]
            health = store.calculate_health_score(account, account_opps)
            results.append((account, health))
    return render_template("search.html", query=query, results=results)


@app.route("/customer/<account_id>")
def customer_detail(account_id):
    account = store.get_account(account_id)
    if not account:
        return "Customer not found", 404

    contacts = store.get_contacts_for_account(account_id)
    opportunities = store.get_opportunities_for_account(account_id)
    parent = store.get_parent_account(account)
    children = store.get_child_accounts(account_id)
    health = store.calculate_health_score(account, opportunities)

    arr = account.contract_value if account.contract_value else 0

    return render_template("customer_detail.html",
                         account=account,
                         contacts=contacts,
                         opportunities=opportunities,
                         parent=parent,
                         children=children,
                         arr=arr,
                         health=health)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
