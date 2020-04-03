import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';

import { UserService, AuthenticationService } from '../_services';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.css']
})
export class BodyComponent implements OnInit {

  currentUser: any;
  users: import("../_models/user").User[];

  constructor(
    private authenticationService: AuthenticationService,
    private userService: UserService
) {
    this.currentUser = this.authenticationService.currentUserValue;
}

ngOnInit() {
    this.loadAllUsers();
}

private loadAllUsers() {
  this.userService.getAll()
      .pipe(first())
      .subscribe(users => this.users = users);
}

}
