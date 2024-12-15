import { createQueryParamsString, fetchHandler } from ".";


export async function getSystems(params: Api.Params) {
    return await fetchHandler<Api.Response.SystemReadList[]>('system/' + createQueryParamsString(params));
}

export async function getSystem(id: number) {
    return await fetchHandler<Api.Response.SystemRead>('system/' + id);
}

export async function updateSystem(id: number, data: any) {

    return await fetchHandler<Api.Response.SystemRead>('system/' + id, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function createSystem(data: any) {
    return await fetchHandler<Api.Response.SystemRead>('system/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function deleteSystem(id: number) {
    return await fetchHandler<Api.Response.Success>('system/' + id, {
        method: 'DELETE',
    });
}

export async function countSystems() {
    return await fetchHandler<number>('system/count/');
}