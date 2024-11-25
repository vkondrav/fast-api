export interface ChatBubbleModel {
    userName: string;
    message: string;
    time: string;
    avatarUrl: string;
    isCurrentUser: boolean;
    moderation_pass: boolean;
}