package com.ministone.android.app.bookscanner;

import com.ministone.android.app.bookscanner.R;

import android.app.ListActivity;
import android.content.ContentUris;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;
import android.widget.SimpleCursorAdapter;

/**
 * User: gjkv86
 * Date: 9/8/11
 * Time: 11:59 PM
 */
public class BookListActivity extends ListActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.booklist);

        // Used to map notes entries from the database to views
/*
        SimpleCursorAdapter adapter = new SimpleCursorAdapter(this, R.layout.noteslist_item, cursor,
                new String[] { Constants.COLUMN_TITLE }, new int[] { android.R.id.text1 });
        setListAdapter(adapter);
*/

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

    @Override
    protected void onStop() {
        super.onStop();    //To change body of overridden methods use File | Settings | File Templates.
    }

    @Override
    protected void onListItemClick(ListView l, View v, int position, long id) {
        Uri uri = ContentUris.withAppendedId(getIntent().getData(), id);

        String action = getIntent().getAction();
/*
        if (Intent.ACTION_PICK.equals(action) || Intent.ACTION_GET_CONTENT.equals(action)) {
            setResult(RESULT_OK, new Intent().setData(uri));
        } else {
            startActivity(new Intent(this.getApplicationContext(),BookInfoActivity.class));
        }
*/
        startActivity(new Intent(Intent.ACTION_VIEW,uri));
    }

}
