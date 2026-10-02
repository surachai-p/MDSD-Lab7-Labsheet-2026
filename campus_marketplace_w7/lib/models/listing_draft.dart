class ListingDraft {
  final String title;
  final String category;
  final String description;

  const ListingDraft({
    required this.title,
    required this.category,
    required this.description,
  });

  factory ListingDraft.fromJson(Map<String, dynamic> json) {
    return ListingDraft(
      title: json['title'] as String? ?? '',
      category: json['category'] as String? ?? 'อื่นๆ',
      description: json['description'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'category': category,
      'description': description,
    };
  }
}
