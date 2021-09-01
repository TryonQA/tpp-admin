import { Role, Selector } from 'testcafe';

var user;
var pwd;
// will read in from local file

const myRole = Role('https://login.microsoftonline.com/', async t => {
    await t
        .typeText('#i0116', user)
        .click('#idSIButton9')
        .typeText('#i0118', pwd)
        .click('#idSIButton9')
        //.click('#idSIButton9') // Stay logged in 'Yes'
        .click('#idBtn_Back'); // Stay logged in 'No'

}, { preserveUrl: true });

fixture 
    .disablePageCaching `Transportation Providers Test Automation`
    .page `https://tpp-qa.americanlogistics.com/providers`
    .beforeEach(async t=> {
        await t
            .useRole(myRole)

            .navigateTo('https://tpp-qa.americanlogistics.com/providers')
            
            //.click('button[class="MuiButtonBase-root MuiButton-root MuiButton-contained jss3 MuiButton-containedPrimary"]')

            .wait(500);

    });


test('filter - clear to transport - 1.1.1', async t => {
    await t
        .click('button[class="MuiButtonBase-root MuiButton-root MuiButton-contained jss3 MuiButton-containedPrimary"]')
        .click('div[class="MuiSelect-root MuiSelect-select MuiSelect-selectMenu MuiInputBase-input MuiInput-input"]')
        .click('li[tabindex="-1"]')

        .expect(Selector('div[class="MuiDataGrid-cell  MuiDataGrid-cellWithRenderer MuiDataGrid-cellLeft"][data-rowindex="0"]').withAttribute('data-field', 'IsClearToTransport').exists).ok();
});