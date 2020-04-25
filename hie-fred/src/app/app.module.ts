import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { FormsModule } from "@angular/forms"

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { loginComponent } from './loginComponent/loginComponent.component';
import { BodyComponent } from './body/body.component';
import { FilterBoxComponent } from './filter-box/filter-box.component';
import { DataBasicComponent } from './data-basic/data-basic.component';
import { DataVisComponent } from './data-vis/data-vis.component';
import { fakeBackendProvider,JwtInterceptor,ErrorInterceptor } from './_helpers'; 

import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

//@NgModule tag means this class is an Angular App Module, which groups together related components
@NgModule({ 
  declarations: [
    AppComponent,
    loginComponent,
    BodyComponent,
    FilterBoxComponent,
    DataBasicComponent,
    DataVisComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },

    fakeBackendProvider //TODO change this when

  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
