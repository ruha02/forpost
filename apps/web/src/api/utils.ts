
export const CheckUrl = (url: string) => {
    if (url.includes('http://') || url.includes('https://')) {
        return url
    } else {
        return 'https://' + url
    }
}