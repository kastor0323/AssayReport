import { StyleSheet } from 'react-native';
import { Theme } from '../../types/theme';

export default function createStyles(theme: Theme) {
  return StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    scrollContainer: {
      flex: 1,
      padding: 16
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: 16,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    headerTitle: {
      fontSize: 18,
      fontWeight: 'bold',
      color: theme.colors.text,
    },
    closeButton: {
      padding: 8,
    },
    saveButton: {
      paddingVertical: 8,
      paddingHorizontal: 16,
      borderRadius: 4,
      backgroundColor: theme.colors.primary,
    },
    saveButtonText: {
      color: 'white',
      fontWeight: 'bold',
    },
    inputGroup: {
      marginBottom: 16,
    },
    label: {
      fontSize: 16,
      fontWeight: '600',
      marginBottom: 8,
      color: theme.colors.text,
    },
    input: {
      borderWidth: 1,
      borderRadius: 8,
      padding: 12,
      fontSize: 16,
      borderColor: theme.colors.border,
      backgroundColor: theme.colors.card,
      color: theme.colors.text,
    },
    textArea: {
      height: 100,
      textAlignVertical: 'top',
    },
    assetsContainer: {
      marginBottom: 32,
    },
    sectionHeader: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: 12,
    },
    percentageTotal: {
      fontSize: 16,
      fontWeight: 'bold',
    },
    itemRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingVertical: 12,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    itemInfo: {
      flex: 1,
    },
    itemName: {
      fontSize: 16,
      fontWeight: '500',
      color: theme.colors.text,
    },
    itemRegion: {
      fontSize: 14,
      marginTop: 4,
      color: theme.colors.text + '80',
    },
    itemActions: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    percentInput: {
      width: 60,
      textAlign: 'right',
      borderWidth: 1,
      borderRadius: 4,
      padding: 8,
      marginRight: 4,
      borderColor: theme.colors.border,
      backgroundColor: theme.colors.card,
      color: theme.colors.text,
    },
    percentSymbol: {
      marginRight: 12,
      fontSize: 16,
      color: theme.colors.text,
    },
    removeButton: {
      padding: 8,
    },
    addButton: {
      borderWidth: 1,
      borderRadius: 8,
      padding: 12,
      alignItems: 'center',
      marginTop: 16,
      borderColor: theme.colors.primary,
    },
    addButtonText: {
      fontSize: 16,
      color: theme.colors.primary,
    },
    searchModalContainer: {
      flex: 1,
      backgroundColor: 'rgba(0,0,0,0.5)',
    },
    searchModal: {
      flex: 1,
      marginTop: 60,
      borderTopLeftRadius: 20,
      borderTopRightRadius: 20,
      backgroundColor: theme.colors.background,
    },
    searchHeader: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: 16,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    searchTitle: {
      fontSize: 18,
      fontWeight: 'bold',
      marginLeft: 16,
      color: theme.colors.text,
    },
    closeSearchButton: {
      padding: 8,
    },
    regionTabs: {
      flexDirection: 'row',
      padding: 16,
    },
    regionTab: {
      flex: 1,
      paddingVertical: 8,
      paddingHorizontal: 12,
      borderRadius: 20,
      alignItems: 'center',
      marginHorizontal: 4,
    },
    regionTabText: {
      fontWeight: '500',
    },
    searchInputContainer: {
      flexDirection: 'row',
      paddingHorizontal: 16,
      marginBottom: 16,
    },
    searchInput: {
      flex: 1,
      borderWidth: 1,
      borderRadius: 8,
      padding: 12,
      fontSize: 16,
      borderColor: theme.colors.border,
      backgroundColor: theme.colors.card,
      color: theme.colors.text,
    },
    searchButton: {
      marginLeft: 8,
      padding: 12,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: theme.colors.primary,
    },
    searchResultItem: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingHorizontal: 16,
      paddingVertical: 12,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    resultItemName: {
      fontSize: 16,
      fontWeight: '500',
      color: theme.colors.text,
    },
    resultItemTicker: {
      fontSize: 14,
      marginTop: 4,
      color: theme.colors.text + '80',
    },
    resultItemPrice: {
      fontSize: 16,
      fontWeight: '500',
      color: theme.colors.text,
    },
    loadingContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      paddingVertical: 32,
    },
    emptyResultContainer: {
      padding: 32,
      alignItems: 'center',
    },
    emptyResultText: {
      fontSize: 16,
      color: theme.colors.text + '80',
    },
  });
} 