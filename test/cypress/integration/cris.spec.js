const baseUrl = Cypress.env('cris_base_url')[Cypress.env('cris_env')]
const SKIP = Cypress.env('cris_skip')
const accounts = Cypress.env('cris_account')

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
      cy.log("Create User "+accounts['user1'].username)
      createUser('user1')
      cy.log("Create User "+accounts['user2'].username)
      createUser('user2')
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Create Datas as Admin', () => {
    if(!SKIP.check){
      cris_login("admin")
      cy.log("Create Institution")
      cy.visit(baseUrl+'/institutions/creation/')
      cy.get('#id_name').type("This is a Test Institution")
      cy.get('#id_pid').type('ark:/testInst1')
      cy.get('.button.is-primary[value="Créer"]').click()
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Create Datas as User 1', () => {
    if(!SKIP.check){
      cris_login("user1")
      cy.log("Create an Article")
      cy.visit(baseUrl+'/articles/creation/')
      cy.get('#id_name').type("This is a Test Article By User 1")
      cy.get('#authorInput').type(accounts['user1'].first_name+" "+accounts['user1'].last_name+", "+accounts['user1'].pid)
      cy.get('#authorInputautocomplete-list div').click()
      cy.get('#id_pid').type('ark:/testArt1')
      cy.get('.button.is-primary[value="Créer"]').click()
      cy.visit(baseUrl+'/projects/creation/')
      cy.get('#id_name').type("This is a Test Project By User 1")
      cy.get('#memberInput').type(accounts['user1'].first_name+" "+accounts['user1'].last_name+", "+accounts['user1'].pid)
      cy.get('#memberInputautocomplete-list div').click()
      cy.get('#id_pid').type('ark:/testProj1')
      cy.get('.button.is-primary[value="Créer"]').click()
      cy.visit(baseUrl+'/datasets/creation/')
      cy.get('#id_name').type("This is a Test Datasets By User 1")
      cy.get('#creatorInput').type(accounts['user1'].first_name+" "+accounts['user1'].last_name+", "+accounts['user1'].pid)
      cy.get('#creatorInputautocomplete-list div').click()
      cy.get('#id_pid').type('ark:/testData1')
      cy.get('.button.is-primary[value="Créer"]').click()
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Create Datas as User 2', () => {
    if(!SKIP.check){
      cris_login("user2")
      cy.log("Create an Article")
      cy.visit(baseUrl+'/articles/creation/')
      cy.get('#id_name').type("This is a Test Article By User 2")
      cy.get('#authorInput').type(accounts['user2'].first_name+" "+accounts['user2'].last_name+", "+accounts['user2'].pid)
      cy.get('#authorInputautocomplete-list div').click()
      cy.get('#id_pid').type('ark:/testArt2')
      cy.get('.button.is-primary[value="Créer"]').click()
      cy.visit(baseUrl+'/projects/creation/')
      cy.get('#id_name').type("This is a Test Project By User 2")
      cy.get('#memberInput').type(accounts['user2'].first_name+" "+accounts['user2'].last_name+", "+accounts['user2'].pid)
      cy.get('#memberInputautocomplete-list div').click()
      cy.get('#id_pid').type('ark:/testProj2')
      cy.get('.button.is-primary[value="Créer"]').click()
      cy.visit(baseUrl+'/datasets/creation/')
      cy.get('#id_name').type("This is a Test Datasets By User 2")
      cy.get('#creatorInput').type(accounts['user2'].first_name+" "+accounts['user2'].last_name+", "+accounts['user2'].pid)
      cy.get('#creatorInputautocomplete-list div').click()
      cy.get('#id_pid').type('ark:/testData2')
      cy.get('.button.is-primary[value="Créer"]').click()
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Check Datas Pages as Admin', () => {
    if(!SKIP.check){
      cris_login("admin")
      cy.visit(baseUrl+'/articles/ark:/testArt1')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 1')
      cy.visit(baseUrl+'/articles/ark:/testArt2')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 2')
      cy.visit(baseUrl+'/projects/ark:/testProj1')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 1')
      cy.visit(baseUrl+'/projects/ark:/testProj2')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 2')
      cy.visit(baseUrl+'/datasets/ark:/testData1')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 1')
      cy.visit(baseUrl+'/datasets/ark:/testData2')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 2')
      cy.visit(baseUrl+'/institutions/ark:/testInst1')
      cy.get('.title.is-4.name').contains('This is a Test Institution')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt1')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 1')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt2')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 2')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj1')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 1')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj2')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 2')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData1')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 1')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData2')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 2')
      cy.visit(baseUrl+'/institutions/edition/ark:/testInst1')
      cy.get('.title.is-4.name').contains('This is a Test Institution')
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Check Datas Pages as Anonymous', () => {
    if(!SKIP.check){
      cy.visit(baseUrl+'/articles/ark:/testArt1')
      acceptCookies()
      cy.get('.title.is-4.name').contains('This is a Test Article By User 1')
      cy.visit(baseUrl+'/articles/ark:/testArt2')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 2')
      cy.visit(baseUrl+'/projects/ark:/testProj1')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 1')
      cy.visit(baseUrl+'/projects/ark:/testProj2')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 2')
      cy.visit(baseUrl+'/datasets/ark:/testData1')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 1')
      cy.visit(baseUrl+'/datasets/ark:/testData2')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 2')
      cy.visit(baseUrl+'/institutions/ark:/testInst1')
      cy.get('.title.is-4.name').contains('This is a Test Institution')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt1')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cet article')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt2')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cet article')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj1')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cet project')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj2')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cet project')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData1')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cet dataset')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData2')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cet dataset')
      cy.visit(baseUrl+'/institutions/edition/ark:/testInst1')
      cy.get('p').contains('Connectez-vous pour pouvoir éditer cette institution')
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Check Datas Pages as User1', () => {
    if(!SKIP.check){
      cris_login("user1")
      cy.visit(baseUrl+'/articles/ark:/testArt1')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 1')
      cy.visit(baseUrl+'/articles/ark:/testArt2')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 2')
      cy.visit(baseUrl+'/projects/ark:/testProj1')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 1')
      cy.visit(baseUrl+'/projects/ark:/testProj2')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 2')
      cy.visit(baseUrl+'/datasets/ark:/testData1')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 1')
      cy.visit(baseUrl+'/datasets/ark:/testData2')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 2')
      cy.visit(baseUrl+'/institutions/ark:/testInst1')
      cy.get('.title.is-4.name').contains('This is a Test Institution')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt1')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 1')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt2')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cet article")
      cy.visit(baseUrl+'/projects/edition/ark:/testProj1')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 1')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj2')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cet project")
      cy.visit(baseUrl+'/datasets/edition/ark:/testData1')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 1')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData2')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cet dataset")
      cy.visit(baseUrl+'/institutions/edition/ark:/testInst1')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cette institution")
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Datas Check Pages as User2', () => {
    if(!SKIP.check){
      cris_login("user2")
      cy.visit(baseUrl+'/articles/ark:/testArt1')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 1')
      cy.visit(baseUrl+'/articles/ark:/testArt2')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 2')
      cy.visit(baseUrl+'/projects/ark:/testProj1')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 1')
      cy.visit(baseUrl+'/projects/ark:/testProj2')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 2')
      cy.visit(baseUrl+'/datasets/ark:/testData1')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 1')
      cy.visit(baseUrl+'/datasets/ark:/testData2')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 2')
      cy.visit(baseUrl+'/institutions/ark:/testInst1')
      cy.get('.title.is-4.name').contains('This is a Test Institution')
      cy.visit(baseUrl+'/articles/edition/ark:/testArt1')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cet article")
      cy.visit(baseUrl+'/articles/edition/ark:/testArt2')
      cy.get('.title.is-4.name').contains('This is a Test Article By User 2')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj1')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cet project")
      cy.visit(baseUrl+'/projects/edition/ark:/testProj2')
      cy.get('.title.is-4.name').contains('This is a Test Project By User 2')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData1')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cet dataset")
      cy.visit(baseUrl+'/datasets/edition/ark:/testData2')
      cy.get('.title.is-4.name').contains('This is a Test Datasets By User 2')
      cy.visit(baseUrl+'/institutions/edition/ark:/testInst1')
      cy.get('p').contains("Vous n'avez pas le droit d'éditer cette institution")
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Edit Datas as Admin', () => {
    if(!SKIP.edition){
      cris_login("admin")
      cy.visit(baseUrl+'/institutions/edition/ark:/testInst1')
      cy.get('.link-one.is-size-6[href="/institutions/edition/field/alternateName/ark:/testInst1"]').click()
      cy.get('#id_alternate_name').type('TestInst1')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is a Test Institution (TestInst1)')
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Edit Datas as User 1', () => {
    if(!SKIP.edition){
      cris_login("user1")
      cy.visit(baseUrl+'/articles/edition/ark:/testArt1')
      cy.get('.link-one[href="/articles/edition/field/name/ark:/testArt1"]').click()
      cy.get('#id_name').type('{selectall}{del}This is an Edited Article by User 1')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is an Edited Article by User 1')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj1')
      cy.get('.link-one[href="/projects/edition/field/name/ark:/testProj1"]').click()
      cy.get('#id_name').type('{selectall}{del}This is an Edited Project by User 1')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is an Edited Project by User 1')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData1')
      cy.get('#myBtn-div').click()
      cy.get('.link-one[href="/datasets/edition/field/name/ark:/testData1"]').click()
      cy.get('#id_name').type('{selectall}{del}This is an Edited Dataset by User 1')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is an Edited Dataset by User 1')
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Edit Datas as User 2', () => {
    if(!SKIP.edition){
      cris_login("user2")
      cy.visit(baseUrl+'/articles/edition/ark:/testArt2')
      cy.get('.link-one[href="/articles/edition/field/name/ark:/testArt2"]').click()
      cy.get('#id_name').type('{selectall}{del}This is an Edited Article by User 2')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is an Edited Article by User 2')
      cy.visit(baseUrl+'/projects/edition/ark:/testProj2')
      cy.get('.link-one[href="/projects/edition/field/name/ark:/testProj2"]').click()
      cy.get('#id_name').type('{selectall}{del}This is an Edited Project by User 2')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is an Edited Project by User 2')
      cy.visit(baseUrl+'/datasets/edition/ark:/testData2')
      cy.get('#myBtn-div').click()
      cy.get('.link-one[href="/datasets/edition/field/name/ark:/testData2"]').click()
      cy.get('#id_name').type('{selectall}{del}This is an Edited Dataset by User 2')
      cy.get('.button.is-primary[value="Modifier"]').click()
      cy.get('.title.is-4.name').contains('This is an Edited Dataset by User 2')
    }else{
      cy.log('SKIPPED')
    }
  })
  it('0x. Delete Datas', () => {
    if(!SKIP.deletion){
      cris_login("admin")
      cy.visit(baseUrl+'/articles/edition/ark:/testArt1')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
      cy.visit(baseUrl+'/articles/edition/ark:/testArt2')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
      cy.visit(baseUrl+'/projects/edition/ark:/testProj1')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
      cy.visit(baseUrl+'/projects/edition/ark:/testProj2')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
      cy.visit(baseUrl+'/datasets/edition/ark:/testData1')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
      cy.visit(baseUrl+'/datasets/edition/ark:/testData2')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
      cy.visit(baseUrl+'/institutions/edition/ark:/testInst1')
      cy.get('.link-one.right-align.little-space-above.mr-5').click()
    }else{
      cy.log('SKIPPED')
    }

  })
  it('0x. Delete Users', () => {
    if(!SKIP.deletion){
      cris_login("admin")
      deleteUser('user1')
      deleteUser('user2')
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
  cy.get('.title.is-4').contains('Connectez-vous')
  cy.get('#id_username').type(accounts[user].username)
  cy.get('#id_password').type(accounts[user].password)
  cy.get('form > .button.is-primary').contains('Connexion').click()
}

function createUser(user){
  cy.visit(baseUrl+'/admin/INCIPIT_CRIS_app/user/add/')
  cy.get('#id_username').type(accounts[user].username)
  cy.get('#id_email').type(accounts[user].email)
  cy.get('#id_first_name').type(accounts[user].first_name)
  cy.get('#id_last_name').type(accounts[user].last_name)
  cy.get('#id_pid').type(accounts[user].pid)
  cy.get('#id_password1').type(accounts[user].password)
  cy.get('#id_password2').type(accounts[user].password)
  cy.get('.default[value="Save"]').click()
  cy.get('.success').contains('The user “'+accounts[user].pid+'” was added successfully. You may edit it again below.')
}

function deleteUser(user){
  cy.visit(baseUrl+'/admin/INCIPIT_CRIS_app/user/')
  cy.get('.field-pid a').contains(accounts[user].pid).click()
  cy.get('.deletelink').contains('Delete').click()
  cy.get('.content').find('input[type="submit"]').click()
  cy.get('li.success').contains('The user “'+accounts[user].pid+'” was deleted successfully.')

}
