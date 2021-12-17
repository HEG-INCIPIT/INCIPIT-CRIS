const baseUrl = Cypress.env('cris_base_url')[Cypress.env('cris_env')]
const SKIP = Cypress.env('cris_skip')

let identifierAnonym=undefined,identifierAdmin=undefined

describe('ARKetype Tests', () => {
    it('01. Check Pages as Anonymous', () => {
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
    it('0x. Check Login and Logout as Admin', () => {
        if(!SKIP.check){
            cris_login("admin")

            cy.get('.button.is-danger').contains('Déconnexion')

            cy.visit(baseUrl+'/logout')
            cy.get('.button.is-primary').contains('Connexion')
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Check Admin Dashboard as Admin', () => {
        if(!SKIP.check){
            cris_login("admin")
            cy.log("Create User1")
            cy.log("Create User2")
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Restore Test Backup as Admin', () => {
        if(!SKIP.check){
            cris_login("admin")
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Create CRIS elements as Admin', () => {
        if(!SKIP.check){
            cris_login("admin")
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Check Pages as Admin', () => {
        if(!SKIP.check){
            cris_login("admin")
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Check Pages as Anonymous', () => {
        if(!SKIP.check){
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Check Pages as #User1', () => {
        if(!SKIP.check){
        }else{
            cy.log('SKIPPED')
        }
    })
    it('0x. Check Pages as #User2', () => {
        if(!SKIP.check){
        }else{
            cy.log('SKIPPED')
        }
    })
})

function acceptCookies(){
    cy.get('.cookiebannerSubmit.btn').contains('Sauvegarder').click()
}
function cris_login(user){
    cy.visit(baseUrl+'/login')
    acceptCookies()
    console.log(Cypress.env('cris_account'))
    cy.get('.title.is-4').contains('Connectez-vous')
    cy.get('#id_username').type(Cypress.env('cris_account')[user]username)
    cy.get('#id_password').type(Cypress.env('cris_account')[user]password)
    cy.get('form > .button.is-primary').contains('Connexion').click()
}
