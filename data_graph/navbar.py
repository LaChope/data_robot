import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(

        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Select Project",
                children=[
                    dbc.DropdownMenuItem("Overview", href='/home'),
                    dbc.DropdownMenuItem("DAI", href='/DAI'),
                    dbc.DropdownMenuItem("MAP", href='/HAFMAP'),
                    dbc.DropdownMenuItem("JLR", href='/JLR'),
                    ],
                ),
            ],
          brand="Home",
          brand_href="/home",
          sticky="top"
    )

    return navbar