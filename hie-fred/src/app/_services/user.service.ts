//from https://github.com/cornflourblue/angular-8-registration-login-example

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { User } from '../_models';

@Injectable({ providedIn: 'root' })
export class UserService {
    constructor(private http: HttpClient) { }

    //we dont know if we need any of this!?

    getAll() {
        return this.http.get<User[]>(`${config.apiUrl}/users`);
    }

    // register(user: User) {
    //     return this.http.post(`${config.apiUrl}/users/register`, user);
    // }

    // delete(id: number) {
    //     return this.http.delete(`${config.apiUrl}/users/${id}`);
    // }
}