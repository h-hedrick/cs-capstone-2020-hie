import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from './_services';

/*
"Angular components can subscribe() to the public currentUser: Observable property 
to be notified of changes, and notifications are sent when the 
this.currentUserSubject.next() method is called in the login() and logout() methods, 
passing the argument to each subscriber."
*/

@Component({
  selector: 'app-root', //name of the <tag> that calls this component
  templateUrl: './app.component.html', //file where <app-root> can be found
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  currentUser: any;
  title = 'hie-fred'; //@hazel does this get used anywhere?? -alice
  loggedIn = false; // how do we make this change?

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService
) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
}

  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}

  //getDefaultData() //does this need to be here too? @