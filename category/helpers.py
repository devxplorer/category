from category.models import Category


def get_categories_original(outfit_id, user_id):
    categories = Category.objects.filter(owner_id=user_id).order_by('id')
    added = categories.extra(select={'added': '1'}).filter(outfits__pk=outfit_id)
    added = list(added.values('added', 'name', 'id'))
    added_f = categories.extra(select={'added': '0'}).exclude(outfits__pk=outfit_id)
    added_f = list(added_f.values('added', 'name', 'id'))
    return added + added_f


def get_categories_raw_sql(outfit_id, user_id):
    q = """\
    SELECT category_category.id,
           category_category.name,
           CASE
                 WHEN COUNT(outfit_id) > 0 THEN 1 ELSE 0
           END as added
    FROM category_category
      LEFT JOIN category_category_outfits 
          ON category_category.id = category_category_outfits.category_id 
             AND category_category_outfits.outfit_id=%s
    WHERE category_category.owner_id=%s
    GROUP BY category_category.id, category_category.name
    ORDER BY category_category.id"""
    categories = Category.objects.raw(q, [outfit_id, user_id])
    return [{'id': c.id, 'name': c.name, 'added': c.added} for c in categories]
