import type {ChatBubbleData} from "@/types/ChatBubbleData";

export interface UIState {
    isLoading: boolean;
    messages: ChatBubbleData[];
}

export const initialState: UIState = {
    isLoading: true,
    messages: []
};