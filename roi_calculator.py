# purchase
value_in_eur = 230000 + 7500        # initial price + restoration, furniture, etc.
down_payment_in_eur = 75000
# mortgage
duration_in_years = 35
interest_rate = 1.03                # meaning 3% on top, as in <loan> x 103%
# rental
operation_cost = 2000/12            # annual operation cost converted to monthly
rent_in_eur = 1200 + operation_cost
# fees
notary_fee_in_eur = 4500            # usually a percent, here it's static
agent_fee = .03                     # meaning 3% (before vat)
# taxes
local_rent_tax_rate = .21           # meaning 21%, it taxes profit after deduction of costs
annual_property_tax_in_eur = 1000   # grundsteuer, imu, etc.
local_registration_tax_rate = 1.09  # meaning 9%, as in <value> x 109%
local_vat = 1.22                    # meaning 22% as in <value> x 122%

# taxes the property
def tax_registration():
    return local_registration_tax_rate*value_in_eur

# taxes property and applies inital fees
def gross_property_cost_in_eur():
    return tax_registration() + notary_fee_in_eur + agent_fee*local_vat*value_in_eur

# money purely lost upon investing (used to calculate recoup time)
def initiation_cost_in_eur():
    return gross_property_cost_in_eur() - value_in_eur

# how much property you own upon investing 
def initial_equity_in_eur():
    return down_payment_in_eur - initiation_cost_in_eur()

# used to calculate monthly mortgage cost
def monthly_mortgage_in_eur():
    loan = gross_property_cost_in_eur() - down_payment_in_eur
    interest_poly = 0
    for n in range(duration_in_years):
        interest_poly += interest_rate**n
    return loan*(interest_rate**duration_in_years)/(12*interest_poly)

# how much property you accrue in a month (to be scaled by  market fluctuation)
def monthly_equity_return_in_eur():
    return value_in_eur/(12*duration_in_years)

def main():
    initiation_c = initiation_cost_in_eur()
    initial_e = initial_equity_in_eur()
    monthly_r = monthly_mortgage_in_eur()
    monthly_e = monthly_equity_return_in_eur()
    gross_monthly_return_in_eur = rent_in_eur - operation_cost - monthly_r - annual_property_tax_in_eur/12
    if (gross_monthly_return_in_eur > 0):
        net_monthly_return_in_eur = gross_monthly_return_in_eur * (1 - local_rent_tax_rate)
    else:
        net_monthly_return_in_eur = gross_monthly_return_in_eur
    net_monthly_return_w_equity_in_eur = net_monthly_return_in_eur + monthly_equity_return_in_eur()
    recoup_initiation_cost_in_years = initiation_cost_in_eur()/(12*net_monthly_return_w_equity_in_eur)
    initiation_cost_recoup_time_months_rem = int((recoup_initiation_cost_in_years * 12) % 12)
    initiation_cost_recoup_time_days_rem = int((recoup_initiation_cost_in_years * 365) % 365 \
        - initiation_cost_recoup_time_months_rem*30)
    roi_wo_equity = 12 * net_monthly_return_in_eur / down_payment_in_eur
    roi = 12 * net_monthly_return_w_equity_in_eur / down_payment_in_eur

    print('initiation cost {:.2f} euro'.format(initiation_c))
    print('initial equity {:.2f} euro'.format(initial_e))
    print('monthly mortgage {:.2f} euro'.format(monthly_r))
    print('gross monthly return {:.2f} euro'.format(gross_monthly_return_in_eur))
    print('monthly equity return {:.2f} euro'.format(monthly_e))
    print('net monthly return {:.2f} euro'.format(net_monthly_return_in_eur))
    print('net monthly return (w/ equity) {:.2f} euro'.format(net_monthly_return_w_equity_in_eur))
    print('initiation cost recoup time {} years {} months and {} days'.format(
        int(recoup_initiation_cost_in_years),
        initiation_cost_recoup_time_months_rem,
        initiation_cost_recoup_time_days_rem))
    print('roi (w/o equity) {:.2f}%'.format(roi_wo_equity*100))
    print('roi (w/ equity) {:.2f}%'.format(roi*100))

if __name__ == '__main__':
    main()
