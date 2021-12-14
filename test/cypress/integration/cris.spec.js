const baseUrl = Cypress.env('cris_base_url')[Cypress.env('cris_env')]
const SKIP = Cypress.env('cris_skip')

let identifierAnonym=undefined,identifierAdmin=undefined

describe('ARKetype Tests', () => {
    it('01. Check Pages', () => {
        if(!SKIP.check){
            cy.visit(baseUrl)
            acceptCookies()
            cy.get('.is-size-2').contains('Bienvenue sur INCIPIT-CRIS, le CRIS de la HEG')
            cy.visit(baseUrl+'/persons')
            cy.get('nav.breadcrumb.has-succeeds-separator.is-size-7 li.is-active').contains('Personnes')
            cy.visit(baseUrl+'/articles')
            cy.get('nav.breadcrumb.has-succeeds-separator.is-size-7 li.is-active').contains('Articles')
            cy.visit(baseUrl+'/projects')
            cy.get('nav.breadcrumb.has-succeeds-separator.is-size-7 li.is-active').contains('Projets')
            cy.visit(baseUrl+'/datasets')
            cy.get('nav.breadcrumb.has-succeeds-separator.is-size-7 li.is-active').contains('Données')
            cy.visit(baseUrl+'/institutions')
            cy.get('nav.breadcrumb.has-succeeds-separator.is-size-7 li.is-active').contains('Institutions')
            cy.visit(baseUrl+'/funders')
            cy.get('nav.breadcrumb.has-succeeds-separator.is-size-7 li.is-active').contains('Bailleurs de fond')
        }else{
            cy.log('SKIPPED')
        }
    })
    it('04. Check Login and Logout as Admin', () => {
        if(!SKIP.check){
            cris_login()

            cy.get('.button.is-danger').contains('Déconnexion')

            cy.visit(baseUrl+'/logout')
            cy.get('.button.is-primary').contains('Connexion')
        }else{
            cy.log('SKIPPED')
        }
    })

})

function acceptCookies(){
    cy.get('.cookiebannerSubmit.btn').contains('Sauvegarder').click()
}
function cris_login(){
    cy.visit(baseUrl+'/login')
    acceptCookies()
    cy.get('.title.is-4').contains('Connectez-vous')
    cy.get('#id_username').type(Cypress.env('cris_account_admin_username'))
    cy.get('#id_password').type(Cypress.env('cris_account_admin_password'))
    cy.get('form > .button.is-primary').contains('Connexion').click()
}
