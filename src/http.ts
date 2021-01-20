import { Config } from "@/config";
import { GraphQLClient } from "graphql-request";
import { getSdk } from "@/generated/graphql";

export * from "@/generated/graphql";

export function saveAuthHeaders(headers: Record<string, string>): void {
    window.localStorage["bettor:headers"] = JSON.stringify(headers);
}

export function getAuthHeaders(): Record<string, string> | undefined {
    const stored = window.localStorage["bettor:headers"];
    if (stored) {
        return JSON.parse(stored);
    }
    return undefined;
}

export function authenticated(): boolean {
    return window.localStorage["bettor:headers"] != null;
}

export function getApi() {
    const gqlc = new GraphQLClient("http://127.0.0.1:5000/v1/graphql", {
        headers: getAuthHeaders(),
    });
    return getSdk(gqlc);
}

export interface OurRequestInfo {
    url: string;
    method?: string;
    data?: any;
    headers?: { [index: string]: string };
}

export async function http<T>(info: OurRequestInfo): Promise<T> {
    let body: string | null = null;
    if (info.data) {
        body = JSON.stringify(info.data);
    }
    const response = await fetch(Config.baseUrl + info.url, {
        method: info.method || "GET",
        mode: "cors",
        headers: Object.assign(
            {
                "Content-Type": "application/json",
            },
            info.headers
        ),
        body: body,
    });
    return await response.json();
}

export async function getLoginUrl(): Promise<string> {
    const response = await http<{ url: string }>({ url: "/v1/login" });
    return response.url;
}

export interface LoginPerson {
    sub: string;
    email: string;
    name: string;
    picture: string;
}

export interface LoginResponse {
    token: string;
    user: LoginPerson;
}

export async function login(code: string): Promise<LoginResponse> {
    const response = await http<LoginResponse>({
        url: "/v1/login",
        method: "POST",
        data: { code: code },
    });
    saveAuthHeaders({
        Authorization: `Bearer ${response.token}`,
    });
    return response;
}
