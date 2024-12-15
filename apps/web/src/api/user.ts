import { createQueryParamsString, fetchHandler } from ".";


export async function getUsers(params: Api.Params) {
    return await fetchHandler<Api.Response.UserReadList[]>('user/' + createQueryParamsString(params));
}

export async function getUser(id: number) {
    return await fetchHandler<Api.Response.UserRead>('user/' + id);
}

export async function updateUser(id: number, data: any) {

    return await fetchHandler<Api.Response.UserRead>('user/' + id, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function createUser(data: any) {
    data['is_verified'] = true;
    return await fetchHandler<Api.Response.UserRead>('user/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function deleteUser(id: number) {
    return await fetchHandler<Api.Response.Success>('user/' + id, {
        method: 'DELETE',
    });
}

export async function countUsers() {
    return await fetchHandler<number>('user/count/');
}