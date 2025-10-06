@CAJAHUANCAYO_LOGIN @pg-Login
Feature: Login APP Caja Huancayo

  Scenario Outline: Login Correcto APP Caja Huancayo
    Given Usuario se encuentra en la APP Caja Huancayo "<datos>"
    When Usuario ingresa su documento "<datos>"
    And Usuario ingresa password "<datos>"
    And da click en ingresar
    Then Se verifica el login al APP Caja Huancayo correcto "<datos>"

  Examples:
    | datos |
    | 1     |
    
