import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BodyComponent } from './body';


const routes: Routes = [
  {path: 'home', component: BodyComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

// export const routingComponents = [BodyComponent];
// ^ if we ever have multiple routes, this will enable
// app.module.ts to import "routingComponents" rather than each individual component we route to
