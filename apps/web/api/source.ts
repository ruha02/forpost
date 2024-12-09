import { fetchHandler, createQueryParamsString } from ".";


export async function getSources (params: Api.Params) {
    return await fetchHandler<Api.Response.SourceReadList[]>('source/' + createQueryParamsString(params));
}

export async function getSource (id: number) {
    return await fetchHandler<Api.Response.SourceRead>('source/' + id);
}

export async function updateSource(id: number, data: any) {

    return await fetchHandler<Api.Response.SourceRead>('source/' + id, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function createSource(data: any) {
    return await fetchHandler<Api.Response.SourceRead>('source/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function deleteSource(id: number) {
    return await fetchHandler<Api.Response.Success>('source/' + id, {
        method: 'DELETE',
    });
}

export async function countSources() {
    return await fetchHandler<number>('source/count/');
}