// 경로: src/styles/components/recordComponent.styles.ts
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f7',
        padding: 16,
    },
    accountCard: {
        backgroundColor: '#ffffff',
        borderRadius: 12,
        padding: 16,
        marginBottom: 16,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        shadowRadius: 2,
        elevation: 2,
    },
    accountHeader: {
        flexDirection: 'row',
        marginBottom: 12,
        alignItems: 'flex-end',
    },
    accountCompanay: {
        fontSize: 16,
        fontWeight: 'bold',
        paddingRight: 5,
    },
    accountNumber: {
        fontSize: 14,
        fontWeight: 'bold',
    },
    infoRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 8,
    },
    infoLabel: {
        fontSize: 14,
        color: '#666666',
    },
    infoValue: {
        fontSize: 14,
        fontWeight: '500',
    },
    positiveValue: {
        color: '#37b24d',
    },
    negativeValue: {
        color: '#f03e3e',
    },
    tableHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#eeeeee',
        marginTop: 8,
    },
    headerText: {
        fontSize: 13,
        fontWeight: '500',
        color: '#666666',
        flex: 1,
        textAlign: 'center',
    },
    recordRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#f0f0f0',
    },
    recordName: {
        fontSize: 13,
        flex: 1,
        paddingRight: 8,
    },
    recordDate: {
        fontSize: 13,
        color: '#666666',
        flex: 1,
        textAlign: 'center',
    },
    recordProfit: {
        fontSize: 13,
        fontWeight: '500',
        flex: 1,
        textAlign: 'right',
    },
    selectedRecord: {
        backgroundColor: '#f0f8ff', // 선택된 기록 행 배경색
    },
    recordDetail: {
        marginTop: 10,
        padding: 12,
        backgroundColor: '#f5f5f5',
        borderRadius: 8,
        borderLeftWidth: 3,
        borderLeftColor: '#4a90e2',
    },
    recordDetailTitle: {
        fontSize: 14,
        fontWeight: 'bold',
        marginBottom: 6,
    },
});
