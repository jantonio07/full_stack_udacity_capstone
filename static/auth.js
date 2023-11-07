class Auth0Control {
  constructor (AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_AUDIENCE) {
    this.AUTH0_DOMAIN = AUTH0_DOMAIN
    this.AUTH0_CLIENT_ID = AUTH0_CLIENT_ID
    this.AUTH0_AUDIENCE = AUTH0_AUDIENCE
    this.auth0Client = null

    this.viewModel = {
      isAuthenticated: ko.observable(false),
      token: ko.observable(''),
      permissions: ko.observableArray([])
    }

    const elMainDiv = document.createElement('div')
    elMainDiv.style.paddingBottom = '5px'
    document.body.appendChild(elMainDiv)

    const elLoginButton = document.createElement('button')
    elLoginButton.id = definitions.id.LOGIN_BUTTON
    elLoginButton.innerText = 'Log in'
    elLoginButton.addEventListener('click', (evt) => {
      evt.preventDefault()
      this.login()
    })
    elLoginButton.setAttribute('data-bind', 'visible: !isAuthenticated()')
    elMainDiv.appendChild(elLoginButton)

    const elLogoutButton = document.createElement('button')
    elLogoutButton.id = definitions.id.LOGOUT_BUTTON
    elLogoutButton.innerText = 'Log out'
    elLogoutButton.setAttribute('data-bind', 'visible: isAuthenticated()')
    elLogoutButton.addEventListener('click', (evt) => {
      evt.preventDefault()
      this.logout()
    })
    elMainDiv.appendChild(elLogoutButton, elMainDiv)

    ko.applyBindings(this.viewModel)

    window.onload = async () => {
      let oAuthenticationData = await this.isAuthenticated()
      if (!oAuthenticationData.bIsAuthenticated) {
        const query = window.location.search
        if (query.includes('code=') && query.includes('state=')) {
          await this.auth0Client.handleRedirectCallback()
          oAuthenticationData = await this.isAuthenticated()
          window.history.replaceState({}, document.title, '/')
        }
      }
    }
    document.body.appendChild(document.createElement('hr'))
  }

  getViewModel () {
    return this.viewModel
  }

  async isAuthenticated () {
    if (this.auth0Client === null) {
      this.auth0Client = await auth0.createAuth0Client({
        domain: this.AUTH0_DOMAIN,
        clientId: this.AUTH0_CLIENT_ID
      })
    }
    const oAuthenticationData = {
      bIsAuthenticated: await this.auth0Client.isAuthenticated()
    }
    if (oAuthenticationData.bIsAuthenticated) {
      const sToken = await this.getToken()
      console.log('USER TOKEN:', sToken)
      this.viewModel.token(sToken)
      oAuthenticationData.sToken = sToken
      oAuthenticationData.oPayload = this.decodePayloadFromJWTToken(sToken)
      if (oAuthenticationData.oPayload) {
        this.viewModel.permissions(oAuthenticationData.oPayload.permissions)
      }
    } else {
      this.viewModel.permissions([])
    }
    this.viewModel.isAuthenticated(oAuthenticationData.bIsAuthenticated)
    return oAuthenticationData
  }

  decodePayloadFromJWTToken (token) {
    try {
      return JSON.parse(atob(token.split('.')[1]))
    } catch (e) {
      return null
    }
  }

  async getToken () {
    const sToken = await this.auth0Client.getTokenSilently({
      authorizationParams: {
        audience: this.AUTH0_AUDIENCE
      }
    })
    return sToken
  }

  async login () {
    await this.auth0Client.loginWithRedirect({
      authorizationParams: {
        redirect_uri: window.location.origin,
        audience: this.AUTH0_AUDIENCE
      }
    })
  }

  async logout () {
    this.auth0Client.logout({
      logoutParams: {
        returnTo: window.location.origin
      }
    })
  }
}
